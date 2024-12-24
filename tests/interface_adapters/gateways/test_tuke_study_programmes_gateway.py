from unittest.mock import create_autospec, AsyncMock, Mock

import pytest

from src.application.interfaces import WebPageLoader, Parser, LanguageParserFactory
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.enums import Language
from src.interface_adapters.exceptions import PageLoadingError
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.gateways.tuke_study_programmes_gateway import ResTukeStudyProgrammesGateway


@pytest.mark.asyncio
async def test_get_by_codes(test_codes: list[str], test_study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> None:
    url_template = "https://res.tuke.sk/api/programme_detail/{code}?lang={lang}"

    loader_mock = create_autospec(WebPageLoader, load=AsyncMock(), spec_set=True)

    page_datas = [page.data for page in test_study_programmes]

    parse_multiple_mock = Mock()
    parse_multiple_mock.return_value = page_datas

    parse_one_mock = Mock(side_effect=page_datas)

    study_programmes_source_mock = create_autospec(
        Parser[str, ResTukeStudyProgrammeData], parse_one=parse_one_mock, parse_multiple=parse_multiple_mock,
        spec_set=True
    )

    factory_mock = create_autospec(
        LanguageParserFactory,
        create=Mock(return_value=study_programmes_source_mock),
        spec_set=True
    )

    gateway = ResTukeStudyProgrammesGateway(
        loader=loader_mock,
        language_parser_factory=factory_mock
    )

    gateway_return_values = await gateway.get_by_codes(test_codes)
    assert gateway_return_values == test_study_programmes

    for test_code in test_codes:
        for language in Language:
            test_url = url_template.format(code=test_code, lang=language.value)
            loader_mock.load.assert_any_call(test_url)


@pytest.mark.asyncio
async def test_get_by_codes_with_exception_during_page_loading(
        test_codes: list[str], test_study_programmes: list[Page[ResTukeStudyProgrammeData]]
) -> None:
    successfully_loaded_pages = [f"page {n} content" for n in range(len(Language) * len(test_codes) - 1)]
    returned_pages = [
        PageLoadingError(),
        *successfully_loaded_pages
    ]
    loader_mock = create_autospec(WebPageLoader, load=AsyncMock(side_effect=returned_pages), spec_set=True)

    parse_multiple_mock = Mock()
    parse_one_mock = Mock()

    study_programmes_source_mock = create_autospec(
        Parser[str, Page[ResTukeStudyProgrammeData]], parse_one=parse_one_mock, parse_multiple=parse_multiple_mock, spec_set=True
    )

    factory_mock = create_autospec(
        LanguageParserFactory,
        create=Mock(return_value=study_programmes_source_mock),
        spec_set=True
    )

    gateway = ResTukeStudyProgrammesGateway(loader=loader_mock, language_parser_factory=factory_mock)
    await gateway.get_by_codes(test_codes)

    try:
        parse_multiple_mock.assert_called_once_with(successfully_loaded_pages)
    except AssertionError:
        for page in successfully_loaded_pages:
            parse_one_mock.assert_any_call(page)

        assert parse_one_mock.call_count == len(successfully_loaded_pages), \
            (f"Expected parse_one_mock to be called {len(successfully_loaded_pages)} times, "
             f"but it was called {parse_one_mock.call_count} times.")

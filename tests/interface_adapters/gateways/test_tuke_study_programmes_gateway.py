from unittest.mock import create_autospec, AsyncMock, Mock

import pytest

from src.interface_adapters.exceptions import PageLoadingError
from src.domain.enums import Language
from src.domain.entities import TukeStudyProgramme
from src.application.interfaces import WebPageLoader, Parser
from src.interface_adapters.gateways.tuke_study_programmes_gateway import TukeStudyProgrammesGateway


@pytest.mark.asyncio
async def test_get_by_codes(test_codes: list[str], test_study_programmes: list[TukeStudyProgramme]) -> None:
    url_template = "https://res.tuke.sk/api/programme_detail/{code}?lang={lang}"

    loader_mock = create_autospec(WebPageLoader, load=AsyncMock(), spec_set=True)

    parse_multiple_mock = Mock()
    parse_multiple_mock.return_value = test_study_programmes

    parse_one_mock = Mock(side_effect=test_study_programmes)

    study_programmes_source_mock = create_autospec(
        Parser[str, TukeStudyProgramme], parse_one=parse_one_mock, parse_multiple=parse_multiple_mock, spec_set=True
    )

    gateway = TukeStudyProgrammesGateway(loader=loader_mock, parser=study_programmes_source_mock)
    gateway_return_values = await gateway.get_by_codes(test_codes)
    assert gateway_return_values == test_study_programmes

    for test_code in test_codes:
        for language in Language:
            test_url = url_template.format(code=test_code, lang=language.value)
            loader_mock.load.assert_any_call(test_url)


@pytest.mark.asyncio
async def test_get_by_codes_with_exception_during_page_loading(
        test_codes: list[str], test_study_programmes: list[TukeStudyProgramme]
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
        Parser[str, TukeStudyProgramme], parse_one=parse_one_mock, parse_multiple=parse_multiple_mock, spec_set=True
    )

    gateway = TukeStudyProgrammesGateway(loader=loader_mock, parser=study_programmes_source_mock)
    await gateway.get_by_codes(test_codes)

    try:
        parse_multiple_mock.assert_called_once_with(successfully_loaded_pages)
    except AssertionError:
        for page in successfully_loaded_pages:
            parse_one_mock.assert_any_call(page)

        assert parse_one_mock.call_count == len(successfully_loaded_pages), \
            (f"Expected parse_one_mock to be called {len(successfully_loaded_pages)} times, "
             f"but it was called {parse_one_mock.call_count} times.")

from typing import Awaitable, Callable, Any

from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.application.interfaces import WebPageLoader, Parser, LanguageParserFactory
from src.interface_adapters.gateways.tuke_study_programmes_gateway import ResTukeStudyProgrammesGateway


class TrackableResTukeStudyProgrammeGateway(ResTukeStudyProgrammesGateway[ResTukeStudyProgrammeData]):
    def __init__(
            self,
            loader: WebPageLoader,
            language_parser_factory: LanguageParserFactory[Parser[str, ResTukeStudyProgrammeData]],
            gathering_function: Callable[..., Awaitable[Any]]
    ) -> None:
        super().__init__(loader, language_parser_factory)
        self._gathering_function = gathering_function

    async def get_by_codes(self, programmes_codes: list[str]) -> list[Page[ResTukeStudyProgrammeData]]:
        gathered_values = await self._gathering_function(
            *self._get_all_pages_loading_coroutines_generator(programmes_codes)
        )
        pages: list[Page[str]] = self._remove_none_values(gathered_values)
        return self._apply_parser(pages)

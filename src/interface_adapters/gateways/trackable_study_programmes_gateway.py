from typing import Awaitable, Callable, Any

from src.application.interfaces import WebPageLoader, Parser
from src.domain.entities.tuke_study_programme import TukeStudyProgramme
from src.interface_adapters.gateways.tuke_study_programmes_gateway import TukeStudyProgrammesGateway


class TrackableTukeStudyProgrammeGateway(TukeStudyProgrammesGateway):
    def __init__(self, loader: WebPageLoader, parser: Parser[str, TukeStudyProgramme],
                 gathering_function: Callable[..., Awaitable[Any]]):
        super().__init__(loader, parser)
        self._gathering_function = gathering_function

    async def get_by_codes(self, programmes_codes: list[str]) -> list[TukeStudyProgramme]:
        pages = await self._gathering_function(*self._get_all_pages_loading_coroutines_generator(programmes_codes))
        return self._parser.parse_multiple(pages)

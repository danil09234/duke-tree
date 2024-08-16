from typing import Awaitable, Callable, Any

from src.application.interfaces import WebPageLoader, Parser
from src.domain.entities.study_programme import StudyProgramme
from src.interface_adapters.gateways.study_programme_gateway import StudyProgrammesGateway


class TrackableStudyProgrammeGateway(StudyProgrammesGateway):
    def __init__(self, loader: WebPageLoader, parser: Parser[str, StudyProgramme],
                 gathering_function: Callable[..., Awaitable[Any]]):
        super().__init__(loader, parser)
        self._gathering_function = gathering_function

    async def get_by_codes(self, programmes_codes: list[str]) -> list[StudyProgramme]:
        pages = await self._gathering_function(*await self._get_all_pages_loading_coroutines(programmes_codes))
        return self._parser.parse_multiple(pages)

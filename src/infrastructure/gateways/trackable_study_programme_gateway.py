from typing import Awaitable, Callable

from src.domain.entities.study_programme import StudyProgramme
from src.infrastructure.gateways.study_programme_gateway import StudyProgrammeGateway, WebPageLoader, Parser


class TrackableStudyProgrammeGateway(StudyProgrammeGateway):
    def __init__(self, loader: WebPageLoader, parser: Parser[str, StudyProgramme],
                 gathering_function: Callable[..., Awaitable]):
        super().__init__(loader, parser)
        self._gathering_function = gathering_function

    async def get_by_codes(self, programmes_codes: list[str]) -> list[StudyProgramme]:
        pages = await self._gathering_function(*await self._get_all_pages_loading_coroutines(programmes_codes))
        return self._parser.parse_multiple(pages)

from pathlib import Path

from src.application.interfaces import Fetchable
from src.domain.entities.government_study_programme import GovernmentStudyProgramme


class StudyProgrammesCodesExcelRepository(Fetchable[GovernmentStudyProgramme]):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    async def fetch_all(self) -> list[GovernmentStudyProgramme]:
        raise NotImplementedError

from pathlib import Path

from src.application.interfaces import Fetchable


class StudyProgrammesCodesExcelRepository(Fetchable[str]):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    async def fetch_all(self) -> list[str]:
        """
        Fetches study programmes codes from an Excel file.

        :return: List of study programmes codes.
        """
        return []

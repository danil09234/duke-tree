from pathlib import Path
from typing import Any, Generator

import openpyxl
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from src.domain.entities.government_study_programme import GovernmentStudyProgramme
from src.application.interfaces import Fetchable
from src.interface_adapters.exceptions import InvalidExcelFileStructure


class StudyProgrammesCodesExcelRepository(Fetchable[GovernmentStudyProgramme]):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    async def fetch_all(self) -> list[GovernmentStudyProgramme]:
        raise NotImplementedError

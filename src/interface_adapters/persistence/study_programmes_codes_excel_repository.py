from pathlib import Path

import openpyxl

from src.application.interfaces import Fetchable
from src.interface_adapters.exceptions import InvalidExcelFileStructure


class StudyProgrammesCodesExcelRepository(Fetchable[str]):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    async def fetch_all(self) -> list[str]:
        programme_codes = []
        wb = openpyxl.load_workbook(self._file_path)
        sheet = wb.active
        max_rows = sheet.max_row

        # Check if the first row is a header
        first_row = [cell.value for cell in sheet[1]]
        has_header = any(isinstance(cell, str) for cell in first_row)
        start_row = 2 if has_header else 1

        for i in range(start_row, max_rows + 1):
            code_cell = sheet.cell(row=i, column=1).value
            if not code_cell and i != max_rows:
                raise InvalidExcelFileStructure(f"Cell A{i} is empty")
            programme_codes.append(code_cell)
        programme_codes = [str(code) for code in programme_codes]

        return programme_codes

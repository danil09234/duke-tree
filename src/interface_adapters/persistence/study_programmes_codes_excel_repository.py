from pathlib import Path
from typing import Any, Generator

import openpyxl
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from src.application.interfaces import Fetchable
from src.interface_adapters.exceptions import InvalidExcelFileStructure


class StudyProgrammesCodesExcelRepository(Fetchable[str]):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    async def fetch_all(self) -> list[str]:
        worksheet = self._get_worksheet()
        programme_codes = self._get_list_of_codes(worksheet)
        return programme_codes

    @classmethod
    def _get_list_of_codes(cls, worksheet: Worksheet) -> list[str]:
        return [str(cell.value) for cell in cls._iter_codes_column(worksheet)]

    @classmethod
    def _iter_codes_column(cls, worksheet: Worksheet) -> Generator[Any, None, None]:
        for current_row in cls._get_rows_range(worksheet):
            current_cell = cls._get_code_cell(worksheet, current_row)
            cls._assert_is_valid_code_cell(current_cell)
            yield current_cell

    @classmethod
    def _get_rows_range(cls, worksheet: Worksheet) -> range:
        has_header = cls._sheet_has_header(worksheet)
        first_row_number = 2 if has_header else 1
        last_row_number = worksheet.max_row + 1
        return range(first_row_number, last_row_number)

    @staticmethod
    def _assert_is_valid_code_cell(code_cell: Cell) -> None:
        if not code_cell.value and code_cell.row != code_cell.parent.max_row:
            raise InvalidExcelFileStructure(f"Cell A{code_cell} is empty")

    @staticmethod
    def _get_code_cell(worksheet: Worksheet, row: int) -> Cell:
        cell: Cell = worksheet.cell(row=row, column=1)
        return cell

    @staticmethod
    def _sheet_has_header(worksheet: Worksheet) -> bool:
        first_row = [cell.value for cell in worksheet[1]]
        has_header = any(isinstance(cell, str) for cell in first_row)
        return has_header

    def _get_worksheet(self) -> Worksheet:
        workbook = openpyxl.load_workbook(self._file_path)
        worksheet: Worksheet = workbook.active
        return worksheet

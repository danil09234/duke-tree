import pytest
from pathlib import Path

from src.interface_adapters.persistence.study_programmes_codes_excel_repository import \
    StudyProgrammesCodesExcelRepository


@pytest.mark.asyncio
@pytest.mark.xfail(raises=NotImplementedError, reason="Not implemented yet")
async def test_fetch_all(study_programmes_excel: Path, study_programmes_codes: list[str]) -> None:
    repository = StudyProgrammesCodesExcelRepository(file_path=study_programmes_excel)
    codes = await repository.fetch_all()
    assert codes == study_programmes_codes

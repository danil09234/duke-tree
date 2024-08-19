import pytest
from pathlib import Path

from src.interface_adapters.exceptions import InvalidExcelFileStructure
from src.interface_adapters.persistence.study_programmes_codes_excel_repository import \
    StudyProgrammesCodesExcelRepository


@pytest.mark.asyncio
@pytest.mark.xfail(raises=NotImplementedError, reason="Not implemented yet")
async def test_fetch_all_standard(
        study_programmes_excel_standard: Path,
        study_programmes_codes_standard: list[str]
) -> None:
    repository = StudyProgrammesCodesExcelRepository(file_path=study_programmes_excel_standard)
    codes = await repository.fetch_all()
    assert codes == study_programmes_codes_standard


@pytest.mark.asyncio
@pytest.mark.xfail(raises=NotImplementedError, reason="Not implemented yet")
async def test_fetch_all_empty_file(study_programmes_excel_empty: Path) -> None:
    repository = StudyProgrammesCodesExcelRepository(file_path=study_programmes_excel_empty)
    codes = await repository.fetch_all()
    assert codes == []


@pytest.mark.asyncio
@pytest.mark.xfail(raises=NotImplementedError, reason="Not implemented yet")
async def test_fetch_all_invalid_file(study_programmes_excel_invalid: Path) -> None:
    repository = StudyProgrammesCodesExcelRepository(file_path=study_programmes_excel_invalid)
    with pytest.raises(InvalidExcelFileStructure):
        await repository.fetch_all()

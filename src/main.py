import asyncio
from pathlib import Path

from interface_adapters.persistence.study_programmes_codes_excel_repository import StudyProgrammesCodesExcelRepository
from src.infrastructure.cli.app import cli


async def main():
    cli()

    # Test extracting study programmes codes from an Excel file

    # file_path = Path("../resources/study_programmes.xlsx")
    # repository = StudyProgrammesCodesExcelRepository(file_path)
    # study_programmes_codes = await repository.fetch_all()
    # with open("programme_codes.txt", "w") as f:
    #     for code in study_programmes_codes:
    #         f.write(f"{code}\n")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from pathlib import Path

import click

from src.application.interfaces import StudyProgrammeSource, Fetchable, Savable, WebPageLoader, Parser
from src.application.use_cases.fetch_and_save_study_programmes import FetchAndSaveStudyProgrammesUseCase
from src.domain.entities.study_programme import StudyProgramme
from src.infrastructure.html_study_programme_parser import HtmlStudyProgrammeParser
from src.infrastructure.persistence.database_repository import PostgresStudyProgrammesRepository
from src.infrastructure.study_programme_gateway import StudyProgrammeGateway
from src.infrastructure.aiohttp_web_page_loader import AiohttpWebPageLoader
from src.infrastructure.study_programmes_codes_excel_repository import StudyProgrammesCodesExcelRepository


@click.group()
def cli():
    pass


@cli.command()
@click.argument("study_programmes_codes_excel_file_path", type=Path)
def save_study_programmes(study_programmes_codes_excel_file_path: Path):
    codes_source: Fetchable[str] = StudyProgrammesCodesExcelRepository(study_programmes_codes_excel_file_path)
    web_page_loader: WebPageLoader = AiohttpWebPageLoader()
    html_parser: Parser[str, StudyProgramme] = HtmlStudyProgrammeParser()
    study_programmes_gateway: StudyProgrammeSource = StudyProgrammeGateway(web_page_loader, html_parser)
    storage: Savable[StudyProgramme] = PostgresStudyProgrammesRepository()
    use_case = FetchAndSaveStudyProgrammesUseCase(codes_source, study_programmes_gateway, storage)
    asyncio.run(use_case())


if __name__ == "__main__":
    cli()

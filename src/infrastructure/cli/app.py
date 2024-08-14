import asyncio
from pathlib import Path

import click

from src.application.interfaces import StudyProgrammeSource, Fetchable, Savable, WebPageLoader, Parser
from src.application.use_cases.fetch_and_save_study_programmes import FetchAndSaveStudyProgrammesUseCase
from src.domain.entities.study_programme import StudyProgramme
from src.infrastructure.parsers.study_programme_html_parser import StudyProgrammeHtmlParser
from src.infrastructure.persistence.postgres_study_programme_repository import PostgresStudyProgrammeRepository
from src.infrastructure.loaders.aiohttp_web_loader import AiohttpWebLoader
from src.infrastructure.persistence.study_programmes_codes_excel_repository import StudyProgrammesCodesExcelRepository
from src.infrastructure.gateways.trackable_study_programme_gateway import TrackableStudyProgrammeGateway

from tqdm.asyncio import tqdm


@click.group()
def cli():
    pass


@cli.command()
@click.argument("study_programmes_codes_excel_file_path", type=Path)
def save_study_programmes(study_programmes_codes_excel_file_path: Path):
    codes_source: Fetchable[str] = StudyProgrammesCodesExcelRepository(study_programmes_codes_excel_file_path)
    web_page_loader: WebPageLoader = AiohttpWebLoader()
    html_parser: Parser[str, StudyProgramme] = StudyProgrammeHtmlParser()
    study_programmes_gateway: StudyProgrammeSource = TrackableStudyProgrammeGateway(
        web_page_loader, html_parser, tqdm.gather
    )
    storage: Savable[StudyProgramme] = PostgresStudyProgrammeRepository()
    use_case = FetchAndSaveStudyProgrammesUseCase(codes_source, study_programmes_gateway, storage)
    asyncio.run(use_case())


if __name__ == "__main__":
    cli()

import asyncio
from pathlib import Path

import click

from src.application.interfaces import StudyProgrammesSource, Fetchable, Savable, WebPageLoader, Parser
from src.application.use_cases.fetch_and_save_study_programmes import FetchAndSaveStudyProgrammesUseCase
from src.domain.entities.study_programme import StudyProgramme
from src.infrastructure.config.sqlalchemy_database_config import SQLAlchemyDatabaseConfig
from src.infrastructure.orm.database_initializer import DatabaseInitializer
from src.infrastructure.orm.factories.engine_factory import EngineFactory
from src.infrastructure.orm.factories.session_maker_factory import SessionMakerFactory
from src.infrastructure.orm.mappers.sqlalchemy_study_programme_mapper import SQLAlchemyStudyProgrammeMapper
from src.infrastructure.orm.models import Base
from src.interface_adapters.parsers.study_programme_html_parser import StudyProgrammeHtmlParser
from src.infrastructure.persistence.sqlalchemy_study_programme_repository import SQLAlchemyStudyProgrammeRepository
from src.infrastructure.loaders.aiohttp_web_loader import AiohttpWebLoader
from src.interface_adapters.persistence.study_programmes_codes_excel_repository import \
    StudyProgrammesCodesExcelRepository
from src.interface_adapters.gateways.trackable_study_programmes_gateway import TrackableStudyProgrammeGateway

from tqdm.asyncio import tqdm  # type: ignore


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("study_programmes_codes_excel_file_path", type=Path)
def save_study_programmes(study_programmes_codes_excel_file_path: Path) -> None:
    database_config = SQLAlchemyDatabaseConfig()
    database_engine_factory = EngineFactory(database_config.async_database_url)
    database_engine = database_engine_factory.create()
    database_session_maker_factory = SessionMakerFactory(database_engine)
    session_maker = database_session_maker_factory.create()
    database_initializer = DatabaseInitializer(
        engine=database_engine, session_maker=session_maker, base=Base, config=database_config
    )
    asyncio.run(database_initializer.init_database())

    codes_source: Fetchable[str] = StudyProgrammesCodesExcelRepository(study_programmes_codes_excel_file_path)
    web_page_loader: WebPageLoader = AiohttpWebLoader()
    html_parser: Parser[str, StudyProgramme] = StudyProgrammeHtmlParser()
    study_programmes_gateway: StudyProgrammesSource = TrackableStudyProgrammeGateway(
        web_page_loader, html_parser, tqdm.gather
    )
    study_programme_mapper = SQLAlchemyStudyProgrammeMapper()
    storage: Savable[StudyProgramme] = SQLAlchemyStudyProgrammeRepository(session_maker, study_programme_mapper)
    use_case = FetchAndSaveStudyProgrammesUseCase(codes_source, study_programmes_gateway, storage)
    asyncio.run(use_case())


if __name__ == "__main__":
    cli()

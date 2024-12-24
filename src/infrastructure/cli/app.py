import asyncio
from pathlib import Path

import click
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from tqdm.asyncio import tqdm  # type: ignore

from src.application.interfaces import (
    StudyProgrammesRepositoryByCodes,
    Fetchable,
    Savable,
    WebPageLoader,
    Parser,
    LanguageParserFactory,
    GetAllRepository, QuestionTreeGraphGenerator,
)
from src.application.use_cases.fetch_and_save_study_programmes import FetchAndSaveStudyProgrammesUseCase
from src.application.use_cases.generate_and_save_questions_tree import GenerateAndSaveQuestionsTreeUseCase
from src.application.use_cases.load_question_trees_and_generate_graphs_use_case import \
    LoadQuestionTreesAndGenerateGraphsUseCase
from src.domain.entities.question_tree import QuestionsTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.infrastructure.config.sqlalchemy_database_config import SQLAlchemyDatabaseConfig
from src.infrastructure.loaders.aiohttp_web_loader import AiohttpWebLoader
from src.infrastructure.orm.database_initializer import DatabaseInitializer
from src.infrastructure.orm.factories.engine_factory import EngineFactory
from src.infrastructure.orm.factories.session_maker_factory import SessionMakerFactory
from src.infrastructure.orm.mappers.sqlalchemy_study_programme_mapper import SQLAlchemyStudyProgrammeMapper
from src.infrastructure.orm.models import Base
from src.infrastructure.persistence.sqlalchemy_study_programme_repository import SQLAlchemyStudyProgrammeRepository
from src.interface_adapters.factories.language_parser_factory import ResTukeLanguageParserFactory
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.gateways.trackable_study_programmes_gateway import TrackableResTukeStudyProgrammeGateway
from src.interface_adapters.persistence.plain_text_repository import PlainTextRepository
from src.interface_adapters.persistence.serializer_storage import SerializerStorage
from src.interface_adapters.persistence.study_programmes_codes_excel_repository import (
    StudyProgrammesCodesExcelRepository
)
from src.interface_adapters.services.mermaid_graph_generator import MermaidGraphGenerator
from src.interface_adapters.services.openai_decision_tree_question_generator import OpenAIDecisionTreeQuestionGenerator
from src.interface_adapters.services.res_tuke_question_tree_generator import ResTukeQuestionTreeGenerator


async def _create_session_maker_and_init_db() -> async_sessionmaker[AsyncSession]:
    database_config = SQLAlchemyDatabaseConfig()
    database_engine = EngineFactory(database_config.async_database_url).create()
    session_maker = SessionMakerFactory(database_engine).create()
    database_initializer = DatabaseInitializer(
        engine=database_engine, session_maker=session_maker, base=Base, config=database_config
    )
    await database_initializer.init_database()
    return session_maker


def _create_session_maker_and_init_db_sync() -> async_sessionmaker[AsyncSession]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_create_session_maker_and_init_db())


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("study_programmes_codes_excel_file_path", type=Path)
def save_study_programmes(study_programmes_codes_excel_file_path: Path) -> None:
    session_maker = _create_session_maker_and_init_db_sync()
    codes_source: Fetchable[str] = StudyProgrammesCodesExcelRepository(study_programmes_codes_excel_file_path)
    web_page_loader: WebPageLoader = AiohttpWebLoader()
    parser_factory: LanguageParserFactory[Parser[str, ResTukeStudyProgrammeData]] = ResTukeLanguageParserFactory()
    study_programmes_gateway: StudyProgrammesRepositoryByCodes[
        Page[ResTukeStudyProgrammeData]
    ] = TrackableResTukeStudyProgrammeGateway(
        web_page_loader, parser_factory, tqdm.gather
    )
    storage: Savable[Page[ResTukeStudyProgrammeData]] = SQLAlchemyStudyProgrammeRepository(
        session_maker, SQLAlchemyStudyProgrammeMapper()
    )
    use_case = FetchAndSaveStudyProgrammesUseCase(codes_source, study_programmes_gateway, storage)
    asyncio.get_event_loop().run_until_complete(use_case())


@cli.command()
@click.argument("openai_api_key", type=str)
@click.argument("destination_file_path", type=Path)
def generate_and_save_questions_tree(openai_api_key: str, destination_file_path: Path) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_build_questions_tree_async(openai_api_key, destination_file_path))


async def _build_questions_tree_async(openai_api_key: str, destination_file_path: Path) -> None:
    session_maker = await _create_session_maker_and_init_db()
    study_programmes_repository = SQLAlchemyStudyProgrammeRepository(session_maker, SQLAlchemyStudyProgrammeMapper())
    llm_decision_tree_question_generator_service = OpenAIDecisionTreeQuestionGenerator(openai_api_key)
    questions_tree_generator = ResTukeQuestionTreeGenerator(llm_decision_tree_question_generator_service)
    questions_tree_storage: Savable[QuestionsTree[Page[ResTukeStudyProgrammeData]]] = (
        SerializerStorage(str(destination_file_path.absolute()))
    )
    use_case = GenerateAndSaveQuestionsTreeUseCase(
        study_programmes_repository,
        questions_tree_generator,
        questions_tree_storage
    )
    await use_case()


@cli.command()
@click.argument("questions_tree_file_path", type=Path)
@click.argument("output_file_path", type=Path)
def generate_graph_from_questions_tree(questions_tree_file_path: Path, output_file_path: Path) -> None:
    questions_tree_storage: GetAllRepository[QuestionsTree[Page[ResTukeStudyProgrammeData]]] = (
        SerializerStorage(str(questions_tree_file_path.absolute()))
    )
    graph_generator: QuestionTreeGraphGenerator[Page[ResTukeStudyProgrammeData]] = MermaidGraphGenerator()
    plain_text_repository = PlainTextRepository(output_file_path)
    use_case = LoadQuestionTreesAndGenerateGraphsUseCase(questions_tree_storage, graph_generator, plain_text_repository)
    asyncio.get_event_loop().run_until_complete(use_case())


if __name__ == "__main__":
    cli()

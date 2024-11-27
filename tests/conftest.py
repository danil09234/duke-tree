import shutil
from pathlib import Path
from typing import Type, AsyncIterator
from unittest.mock import create_autospec

import pytest
import pytest_asyncio
from _pytest.tmpdir import TempPathFactory
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page, PageMetadata
from src.domain.enums import Language, StudyForm, Degree
from src.infrastructure.interfaces import DatabaseConfig
from src.infrastructure.orm.database_initializer import DatabaseInitializer
from src.infrastructure.orm.factories.engine_factory import EngineFactory
from src.infrastructure.orm.factories.session_maker_factory import SessionMakerFactory
from src.infrastructure.orm.mappers.sqlalchemy_study_programme_mapper import SQLAlchemyStudyProgrammeMapper
from src.infrastructure.orm.models import Base
from src.infrastructure.persistence.sqlalchemy_study_programme_repository import SQLAlchemyStudyProgrammeRepository
from src.interface_adapters.interfaces import Logger
from testcontainers.postgres import PostgresContainer  # type: ignore


class TestDatabaseConfig(DatabaseConfig[Type[DeclarativeBase]]):
    def __init__(self, sync_url: str, async_url: str) -> None:
        self._sync_url = sync_url
        self._async_url = async_url

    @property
    def sync_database_url(self) -> str:
        return self._sync_url

    @property
    def async_database_url(self) -> str:
        return self._async_url

    @property
    def defaults(self) -> list[Type[DeclarativeBase]]:
        return []


@pytest.fixture
def test_study_programme() -> Page[ResTukeStudyProgrammeData]:
    return Page(
        data=ResTukeStudyProgrammeData(
            name="Programme 1 EN",
            study_field="Computer Science",
            level_of_degree=1,
            study_form=StudyForm.PRESENT,
            degree=Degree.BACHELOR,
            length_of_study_in_years=3,
            professionally_oriented=False,
            joint_study_program=False,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 1 EN",
            learning_objectives="Learning objectives of Programme 1 EN",
            main_learning_outcomes="Main learning outcomes of Programme 1 EN",
            faculty="Faculty 1"
        ),
        metadata=PageMetadata(
            url="https://res.tuke.sk/api/programme_detail/SP001?lang=en",
            language=Language.ENGLISH,
            code="SP001",
        )
    )


@pytest.fixture(scope="session")
def test_study_programmes() -> list[Page[ResTukeStudyProgrammeData]]:
    return [
        Page(
            data=ResTukeStudyProgrammeData(
                name="Programme 1 EN",
                study_field="Computer Science",
                level_of_degree=1,
                study_form=StudyForm.PRESENT,
                degree=Degree.BACHELOR,
                length_of_study_in_years=3,
                professionally_oriented=False,
                joint_study_program=False,
                languages_of_delivery=Language.ENGLISH,
                description="Description of Programme 1 EN",
                learning_objectives="Learning objectives of Programme 1 EN",
                main_learning_outcomes="Main learning outcomes of Programme 1 EN",
                faculty="Faculty 1"
            ),
            metadata=PageMetadata(
                url="https://res.tuke.sk/api/programme_detail/SP001?lang=en",
                language=Language.ENGLISH,
                code="SP001",
            )
        ),
        Page(
            data=ResTukeStudyProgrammeData(
                name="Programme 2 EN",
                study_field="Mechanical Engineering",
                level_of_degree=2,
                study_form=StudyForm.PRESENT,
                degree=Degree.MASTER,
                length_of_study_in_years=2,
                professionally_oriented=True,
                joint_study_program=True,
                languages_of_delivery=Language.ENGLISH,
                description="Description of Programme 2 EN",
                learning_objectives="Learning objectives of Programme 2 EN",
                main_learning_outcomes="Main learning outcomes of Programme 2 EN",
                faculty="Faculty 2"
            ),
            metadata=PageMetadata(
                url="https://res.tuke.sk/api/programme_detail/SP002?lang=en",
                language=Language.ENGLISH,
                code="SP002",
            )
        ),
        Page(
            data=ResTukeStudyProgrammeData(
                name="Programme 3 EN",
                study_field="Business Administration",
                level_of_degree=1,
                study_form=StudyForm.PRESENT,
                degree=Degree.BACHELOR,
                length_of_study_in_years=4,
                professionally_oriented=False,
                joint_study_program=False,
                languages_of_delivery=Language.ENGLISH,
                description="Description of Programme 3 EN",
                learning_objectives="Learning objectives of Programme 3 EN",
                main_learning_outcomes="Main learning outcomes of Programme 3 EN",
                faculty="Faculty 3"
            ),
            metadata=PageMetadata(
                url="https://res.tuke.sk/api/programme_detail/SP003?lang=en",
                language=Language.ENGLISH,
                code="SP003",
            )
        ),
        Page(
            data=ResTukeStudyProgrammeData(
                name="Programme 1 SK",
                study_field="Computer Science",
                level_of_degree=1,
                study_form=StudyForm.PRESENT,
                degree=Degree.BACHELOR,
                length_of_study_in_years=3,
                professionally_oriented=False,
                joint_study_program=False,
                languages_of_delivery=Language.SLOVAK,
                description="Description of Programme 1 SK",
                learning_objectives="Learning objectives of Programme 1 SK",
                main_learning_outcomes="Main learning outcomes of Programme 1 SK",
                faculty="Faculty 1"
            ),
            metadata=PageMetadata(
                url="https://res.tuke.sk/api/programme_detail/SP001?lang=sk",
                language=Language.SLOVAK,
                code="SP001",
            )
        ),
        Page(
            data=ResTukeStudyProgrammeData(
                name="Programme 2 SK",
                study_field="Mechanical Engineering",
                level_of_degree=2,
                study_form=StudyForm.PRESENT,
                degree=Degree.MASTER,
                length_of_study_in_years=2,
                professionally_oriented=True,
                joint_study_program=True,
                languages_of_delivery=Language.SLOVAK,
                description="Description of Programme 2 SK",
                learning_objectives="Learning objectives of Programme 2 SK",
                main_learning_outcomes="Main learning outcomes of Programme 2 SK",
                faculty="Faculty 2"
            ),
            metadata=PageMetadata(
                url="https://res.tuke.sk/api/programme_detail/SP002?lang=sk",
                language=Language.SLOVAK,
                code="SP002",
            )
        ),
        Page(
            data=ResTukeStudyProgrammeData(
                name="Programme 3 SK",
                study_field="Business Administration",
                level_of_degree=1,
                study_form=StudyForm.PRESENT,
                degree=Degree.BACHELOR,
                length_of_study_in_years=4,
                professionally_oriented=False,
                joint_study_program=False,
                languages_of_delivery=Language.SLOVAK,
                description="Description of Programme 3 SK",
                learning_objectives="Learning objectives of Programme 3 SK",
                main_learning_outcomes="Main learning outcomes of Programme 3 SK",
                faculty="Faculty 3"
            ),
            metadata=PageMetadata(
                url="https://res.tuke.sk/api/programme_detail/SP003?lang=sk",
                language=Language.SLOVAK,
                code="SP003",
            )
        )
    ]


@pytest.fixture(scope="session")
def test_codes() -> list[str]:
    return ["SP001", "SP002", "SP003"]


@pytest.fixture
def mapper() -> SQLAlchemyStudyProgrammeMapper:
    return SQLAlchemyStudyProgrammeMapper()


@pytest_asyncio.fixture
async def async_session_maker() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    with PostgresContainer("postgres:16", driver="asyncpg") as postgres:
        database_config = TestDatabaseConfig(
            sync_url=postgres.get_connection_url(driver=None),
            async_url=postgres.get_connection_url(driver="asyncpg")
        )

        database_engine_factory = EngineFactory(database_config.async_database_url)
        database_engine = database_engine_factory.create()
        database_session_maker_factory = SessionMakerFactory(database_engine)
        session_maker = database_session_maker_factory.create()
        database_initializer = DatabaseInitializer(
            engine=database_engine, session_maker=session_maker, base=Base, config=database_config,
            logger=create_autospec(Logger)
        )
        await database_initializer.init_database(fresh_init=True)
        yield session_maker


@pytest.fixture
def repository(
        async_session_maker: async_sessionmaker[AsyncSession],
        mapper: SQLAlchemyStudyProgrammeMapper
) -> SQLAlchemyStudyProgrammeRepository:
    return SQLAlchemyStudyProgrammeRepository(
        session_maker=async_session_maker,
        study_programme_mapper=mapper
    )


@pytest.fixture
def study_programmes_excel_standard(tmp_path: Path) -> Path:
    return copy_file_in_tmp_path(Path("tests/resources/study_programmes_standard.xlsx"), tmp_path)


@pytest.fixture
def study_programmes_codes_standard() -> list[str]:
    return [
        "183878", "183842", "183841", "184093", "184100", "184098", "185072", "184092", "185071", "136215",
        "136229", "100978", "183568", "136254", "136253", "183559", "183569", "100985", "184622", "183596"
    ]


@pytest.fixture
def study_programmes_excel_empty(tmp_path: Path) -> Path:
    return copy_file_in_tmp_path(Path("tests/resources/study_programmes_empty.xlsx"), tmp_path)


@pytest.fixture
def study_programmes_excel_invalid(tmp_path: Path) -> Path:
    return copy_file_in_tmp_path(Path("tests/resources/study_programmes_invalid.xlsx"), tmp_path)


@pytest.fixture(scope="class")
def res_tuke_test_page_sk(tmp_path_factory: TempPathFactory) -> Path:
    tmp_dir = tmp_path_factory.mktemp("res_tuke_sk")
    return copy_file_in_tmp_path(Path("tests/resources/res_tuke_test_page_sk.html"), tmp_dir)


@pytest.fixture(scope="class")
def res_tuke_test_page_en(tmp_path_factory: TempPathFactory) -> Path:
    tmp_dir = tmp_path_factory.mktemp("res_tuke_en")
    source_file = Path("tests/resources/res_tuke_test_page_en.html")
    return copy_file_in_tmp_path(source_file, tmp_dir)


def copy_file_in_tmp_path(source_file_path: Path, tmp_path: Path) -> Path:
    temp_file_path = tmp_path / source_file_path.name
    shutil.copy(source_file_path, temp_file_path)
    return temp_file_path

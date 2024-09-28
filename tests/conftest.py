import shutil
from pathlib import Path
from typing import Type, AsyncIterator
from unittest.mock import create_autospec

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.domain.entities import StudyProgramme
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
def test_study_programme() -> StudyProgramme:
    return StudyProgramme(
        page_url="https://example.com/programme",
        page_language=Language.ENGLISH,
        name="Programme",
        study_field="Computer Science",
        level_of_degree=1,
        study_form=StudyForm.PRESENT,
        degree=Degree.BACHELOR,
        length_of_study_in_years=3,
        professionally_oriented=False,
        joint_study_program=False,
        languages_of_delivery=Language.ENGLISH,
        description="Description of Programme",
        learning_objectives="Learning objectives of Programme",
        main_learning_outcomes="Main learning outcomes of Programme"
    )


@pytest.fixture
def test_study_programmes() -> list[StudyProgramme]:
    return [
        StudyProgramme(
            page_url="https://example.com/programme1",
            page_language=Language.ENGLISH,
            name="Programme 1",
            study_field="Computer Science",
            level_of_degree=1,
            study_form=StudyForm.PRESENT,
            degree=Degree.BACHELOR,
            length_of_study_in_years=3,
            professionally_oriented=False,
            joint_study_program=False,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 1",
            learning_objectives="Learning objectives of Programme 1",
            main_learning_outcomes="Main learning outcomes of Programme 1"
        ),
        StudyProgramme(
            page_url="https://example.com/programme2",
            page_language=Language.ENGLISH,
            name="Programme 2",
            study_field="Mechanical Engineering",
            level_of_degree=2,
            study_form=StudyForm.PRESENT,
            degree=Degree.MASTER,
            length_of_study_in_years=2,
            professionally_oriented=True,
            joint_study_program=True,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 2",
            learning_objectives="Learning objectives of Programme 2",
            main_learning_outcomes="Main learning outcomes of Programme 2"
        ),
        StudyProgramme(
            page_url="https://example.com/programme3",
            page_language=Language.ENGLISH,
            name="Programme 3",
            study_field="Business Administration",
            level_of_degree=1,
            study_form=StudyForm.PRESENT,
            degree=Degree.BACHELOR,
            length_of_study_in_years=4,
            professionally_oriented=False,
            joint_study_program=False,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 3",
            learning_objectives="Learning objectives of Programme 3",
            main_learning_outcomes="Main learning outcomes of Programme 3"
        ),
        StudyProgramme(
            page_url="https://example.com/programme4",
            page_language=Language.ENGLISH,
            name="Programme 4",
            study_field="Electrical Engineering",
            level_of_degree=2,
            study_form=StudyForm.PRESENT,
            degree=Degree.MASTER,
            length_of_study_in_years=2,
            professionally_oriented=True,
            joint_study_program=True,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 4",
            learning_objectives="Learning objectives of Programme 4",
            main_learning_outcomes="Main learning outcomes of Programme 4"
        ),
        StudyProgramme(
            page_url="https://example.com/programme5",
            page_language=Language.ENGLISH,
            name="Programme 5",
            study_field="Civil Engineering",
            level_of_degree=1,
            study_form=StudyForm.PRESENT,
            degree=Degree.BACHELOR,
            length_of_study_in_years=3,
            professionally_oriented=False,
            joint_study_program=False,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 5",
            learning_objectives="Learning objectives of Programme 5",
            main_learning_outcomes="Main learning outcomes of Programme 5"
        ),
        StudyProgramme(
            page_url="https://example.com/programme6",
            page_language=Language.ENGLISH,
            name="Programme 6",
            study_field="Architecture",
            level_of_degree=2,
            study_form=StudyForm.PRESENT,
            degree=Degree.MASTER,
            length_of_study_in_years=2,
            professionally_oriented=True,
            joint_study_program=True,
            languages_of_delivery=Language.ENGLISH,
            description="Description of Programme 6",
            learning_objectives="Learning objectives of Programme 6",
            main_learning_outcomes="Main learning outcomes of Programme 6"
        )
    ]


@pytest.fixture
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


def copy_file_in_tmp_path(source_file_path: Path, tmp_path: Path) -> Path:
    temp_file_path = tmp_path / source_file_path.name
    shutil.copy(source_file_path, temp_file_path)
    return temp_file_path

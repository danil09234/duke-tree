import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.infrastructure.persistence.sqlalchemy_study_programme_repository import SQLAlchemyStudyProgrammeRepository
from src.infrastructure.orm.models import StudyProgramme as StudyProgrammeORM


@pytest_asyncio.fixture
async def saved_single_programme(
        repository: SQLAlchemyStudyProgrammeRepository,
        async_session_maker: async_sessionmaker[AsyncSession],
        test_study_programme: Page[ResTukeStudyProgrammeData]
) -> StudyProgrammeORM:
    await repository.save(test_study_programme)

    async with async_session_maker() as session:
        result = await session.execute(
            select(StudyProgrammeORM).where(StudyProgrammeORM.name == test_study_programme.data.name)
        )
        saved_programme = result.scalar_one_or_none()
        assert saved_programme is not None
    return saved_programme


@pytest_asyncio.fixture
async def saved_multiple_programmes(
        repository: SQLAlchemyStudyProgrammeRepository,
        async_session_maker: async_sessionmaker[AsyncSession],
        test_study_programmes: list[Page[ResTukeStudyProgrammeData]]
) -> list[StudyProgrammeORM]:
    await repository.save_multiple(test_study_programmes)

    async with async_session_maker() as session:
        result = await session.execute(select(StudyProgrammeORM))
        saved_programmes = result.scalars().all()
    return list(saved_programmes)


class TestSQLAlchemyStudyProgrammeRepository:

    @pytest.mark.asyncio
    async def test_save_single_name(
            self,
            test_study_programme: Page[ResTukeStudyProgrammeData],
            saved_single_programme: StudyProgrammeORM
    ) -> None:
        assert saved_single_programme.name == test_study_programme.data.name

    @pytest.mark.asyncio
    async def test_save_single_page_url(
            self,
            test_study_programme: Page[ResTukeStudyProgrammeData],
            saved_single_programme: StudyProgrammeORM
    ) -> None:
        assert saved_single_programme.page_url == test_study_programme.metadata.url

    @pytest.mark.asyncio
    async def test_save_single_page_language(
            self,
            test_study_programme: Page[ResTukeStudyProgrammeData],
            saved_single_programme: StudyProgrammeORM
    ) -> None:
        assert saved_single_programme.page_language.value == test_study_programme.data.languages_of_delivery.value

    @pytest.mark.asyncio
    async def test_save_single_study_field(
            self,
            test_study_programme: Page[ResTukeStudyProgrammeData],
            saved_single_programme: StudyProgrammeORM
    ) -> None:
        assert saved_single_programme.study_field == test_study_programme.data.study_field

    @pytest.mark.asyncio
    async def test_save_multiple_count(
            self,
            test_study_programmes: list[Page[ResTukeStudyProgrammeData]],
            saved_multiple_programmes: list[StudyProgrammeORM]
    ) -> None:
        assert len(saved_multiple_programmes) == len(test_study_programmes)

    @pytest.mark.asyncio
    async def test_save_multiple_names(
            self,
            test_study_programmes: list[Page[ResTukeStudyProgrammeData]],
            saved_multiple_programmes: list[StudyProgrammeORM]
    ) -> None:
        for test_programme, saved_programme in zip(test_study_programmes, saved_multiple_programmes):
            assert saved_programme.name == test_programme.data.name

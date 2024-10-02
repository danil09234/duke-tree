import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from tests.common.assert_study_programme_entity_equals_orm import assert_study_programme_entity_equals_orm
from src.infrastructure.persistence.sqlalchemy_study_programme_repository import SQLAlchemyStudyProgrammeRepository
from src.infrastructure.orm.models import StudyProgramme as StudyProgrammeORM
from src.domain.entities.tuke_study_programme import TukeStudyProgramme


@pytest.mark.asyncio
async def test_save_single_study_programme(
        repository: SQLAlchemyStudyProgrammeRepository,
        async_session_maker: async_sessionmaker[AsyncSession],
        test_study_programme: TukeStudyProgramme
) -> None:
    await repository.save(test_study_programme)

    async with async_session_maker() as session:
        result = await session.execute(
            select(StudyProgrammeORM).where(StudyProgrammeORM.name == test_study_programme.name)
        )
        saved_programme = result.scalar()
        assert saved_programme is not None

        assert_study_programme_entity_equals_orm(test_study_programme, saved_programme)


@pytest.mark.asyncio
async def test_save_multiple_study_programmes(
        repository: SQLAlchemyStudyProgrammeRepository,
        async_session_maker: async_sessionmaker[AsyncSession],
        test_study_programmes: list[TukeStudyProgramme]
) -> None:
    await repository.save_multiple(test_study_programmes)

    async with async_session_maker() as session:
        result = await session.execute(select(StudyProgrammeORM))
        saved_programmes = result.scalars().all()

        for index, study_programme in enumerate(test_study_programmes):
            assert_study_programme_entity_equals_orm(study_programme, saved_programmes[index])

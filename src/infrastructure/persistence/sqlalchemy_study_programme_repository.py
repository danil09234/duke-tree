from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.infrastructure.interfaces import EntityMapper
from src.application.interfaces import Savable
from src.infrastructure.orm.models import StudyProgramme as StudyProgrammeORM


class SQLAlchemyStudyProgrammeRepository(Savable[Page[ResTukeStudyProgrammeData]]):
    def __init__(
            self,
            session_maker: async_sessionmaker[AsyncSession],
            study_programme_mapper: EntityMapper[Page[ResTukeStudyProgrammeData], StudyProgrammeORM]
    ):
        self._session_maker = session_maker
        self._study_programme_mapper = study_programme_mapper

    async def save(self, study_programme: Page[ResTukeStudyProgrammeData]) -> None:
        model = await self._study_programme_mapper.from_entity(study_programme)
        async with self._session_maker() as session:
            session.add(model)
            await session.commit()

    async def save_multiple(self, study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> None:
        models = [
            await self._study_programme_mapper.from_entity(study_programme)
            for study_programme in study_programmes
        ]
        async with self._session_maker() as session:
            session.add_all(models)
            await session.commit()

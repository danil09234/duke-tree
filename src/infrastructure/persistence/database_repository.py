from src.database.models import StudyProgramme
from src.domain.entities.study_programme import StudyProgramme
from src.infrastructure.interfaces import Savable


class PostgresStudyProgrammesRepository(Savable[StudyProgramme]):
    async def save_multiple(self, study_programmes: list[StudyProgramme]) -> None:
        # TODO: Implement saving to the Postgres database using the outer layer of the application
        pass

from unittest.mock import AsyncMock, create_autospec

import pytest

from src.application.interfaces import Fetchable, StudyProgrammesRepositoryByCodes, Savable
from src.application.use_cases.fetch_and_save_study_programmes import FetchAndSaveStudyProgrammesUseCase
from src.domain.entities.tuke_study_programme import TukeStudyProgramme


@pytest.mark.asyncio
async def test_fetch_and_save_study_programmes_use_case(
        test_codes: list[str],
        test_study_programmes: list[TukeStudyProgramme]
) -> None:
    codes_source_mock = create_autospec(Fetchable[str], fetch_all=AsyncMock(), spec_set=True)
    study_programmes_repository_mock = create_autospec(StudyProgrammesRepositoryByCodes, get_by_codes=AsyncMock(), spec_set=True)
    storage_mock = create_autospec(Savable[TukeStudyProgramme], save_multiple=AsyncMock(), spec_set=True)

    codes_source_mock.fetch_all.return_value = test_codes
    study_programmes_repository_mock.get_by_codes.return_value = test_study_programmes

    use_case = FetchAndSaveStudyProgrammesUseCase(
        codes_source=codes_source_mock,
        study_programmes_repository=study_programmes_repository_mock,
        storage=storage_mock
    )

    await use_case()

    codes_source_mock.fetch_all.assert_called_once()
    study_programmes_repository_mock.get_by_codes.assert_called_once_with(test_codes)
    storage_mock.save_multiple.assert_called_once_with(test_study_programmes)

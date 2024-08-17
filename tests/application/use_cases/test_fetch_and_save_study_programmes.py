import pytest
from unittest.mock import AsyncMock, create_autospec

from src.application.interfaces import Fetchable, StudyProgrammesSource, Savable
from src.application.use_cases.fetch_and_save_study_programmes import FetchAndSaveStudyProgrammesUseCase
from src.domain.entities.study_programme import StudyProgramme
from src.domain.enums import StudyForm, Degree, Language


@pytest.mark.asyncio
async def test_fetch_and_save_study_programmes() -> None:
    codes = ["SP001", "SP002", "SP003"]
    study_programmes = [
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
        )
    ]

    codes_source_mock = create_autospec(Fetchable[str], fetch_all=AsyncMock(), spec_set=True)
    study_programmes_source_mock = create_autospec(StudyProgrammesSource, get_by_codes=AsyncMock(), spec_set=True)
    storage_mock = create_autospec(Savable[StudyProgramme], save_multiple=AsyncMock(), spec_set=True)

    codes_source_mock.fetch_all.return_value = codes
    study_programmes_source_mock.get_by_codes.return_value = study_programmes

    use_case = FetchAndSaveStudyProgrammesUseCase(
        codes_source=codes_source_mock,
        study_programmes_source=study_programmes_source_mock,
        storage=storage_mock
    )

    await use_case()

    codes_source_mock.fetch_all.assert_called_once()
    study_programmes_source_mock.get_by_codes.assert_called_once_with(codes)
    storage_mock.save_multiple.assert_called_once_with(study_programmes)

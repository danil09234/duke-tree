from src.domain.entities import StudyProgramme
from src.infrastructure.orm.models import StudyProgramme as StudyProgrammeORM


def assert_study_programme_entity_equals_orm(
        study_programme: StudyProgramme,
        orm_study_programme: StudyProgrammeORM
) -> None:
    assert orm_study_programme.name == study_programme.name
    assert orm_study_programme.page_url == study_programme.page_url
    assert orm_study_programme.page_language.value == study_programme.page_language.value
    assert orm_study_programme.study_field == study_programme.study_field
    assert orm_study_programme.level_of_degree == study_programme.level_of_degree
    assert orm_study_programme.study_form.value == study_programme.study_form.value
    assert orm_study_programme.degree.value == study_programme.degree.value
    assert orm_study_programme.length_of_study_in_years == study_programme.length_of_study_in_years
    assert orm_study_programme.professionally_oriented == study_programme.professionally_oriented
    assert orm_study_programme.joint_study_program == study_programme.joint_study_program
    assert orm_study_programme.languages_of_delivery.value == study_programme.languages_of_delivery.value
    assert orm_study_programme.description == study_programme.description
    assert orm_study_programme.learning_objectives == study_programme.learning_objectives
    assert orm_study_programme.main_learning_outcomes == study_programme.main_learning_outcomes

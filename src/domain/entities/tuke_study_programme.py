from typing import NamedTuple

from src.domain.enums import Degree, Language, StudyForm


class TukeStudyProgramme(NamedTuple):
    """
    A data structure for storing study programme data, which TUKE university provides.
    """

    page_url: str
    page_language: Language
    name: str
    programme_code: int
    study_field: str
    level_of_degree: int
    study_form: StudyForm
    degree: Degree
    length_of_study_in_years: int
    professionally_oriented: bool
    joint_study_program: bool
    languages_of_delivery: Language
    description: str
    learning_objectives: str
    main_learning_outcomes: str
    faculty: str

from typing import NamedTuple


class StudyProgramme(NamedTuple):
    """
    A intermediate data structure for storing parsed study programme data.
    """

    page_url: str
    name: str
    study_field: str
    level_of_degree: int
    study_form: str
    degree: str
    length_of_study_in_years: int
    professionally_oriented: bool
    joint_study_program: bool
    languages_of_delivery: int
    description: str

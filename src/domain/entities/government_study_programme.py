import datetime
from typing import NamedTuple

from src.domain.enums import Degree, StudyForm, Language


class GovernmentStudyProgramme(NamedTuple):
    code: str
    name: str
    level_of_degree: int
    degree: Degree
    study_form: StudyForm
    length_of_study_in_years: int
    university_name: str
    place_of_study: str | None
    faculty_name: str
    field_of_study: list[str]
    languages_of_delivery: Language
    professionally_oriented: bool
    joint_study_program: bool
    first_accreditation: datetime.date
    accreditation_due_limit: datetime.date | None
    decision_number: str | None
    date_of_issue: datetime.date
    type_of_decision: str | None
    note: str | None

from typing import NamedTuple

from src.domain.entities.binary_question import BinaryQuestion


class AnswerOption[StudyProgrammeData](NamedTuple):
    text: str
    answer_node: "OptionsQuestion[StudyProgrammeData]" | BinaryQuestion[StudyProgrammeData] | StudyProgrammeData


class OptionsQuestion[StudyProgrammeData](NamedTuple):
    text: str
    answer_options: list[AnswerOption[StudyProgrammeData]]

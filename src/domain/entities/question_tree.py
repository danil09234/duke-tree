from typing import NamedTuple

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion


class QuestionTree[StudyProgrammeData](NamedTuple):
    root: OptionsQuestion[StudyProgrammeData] | BinaryQuestion[StudyProgrammeData] | StudyProgrammeData


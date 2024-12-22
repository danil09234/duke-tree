from typing import NamedTuple

from src.domain.entities.binary_question import BinaryQuestion


class QuestionsTree[StudyProgrammeData](NamedTuple):
    root: BinaryQuestion[StudyProgrammeData] | StudyProgrammeData

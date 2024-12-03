from typing import NamedTuple

from src.domain.entities.question import Question


class QuestionsTree[StudyProgrammeData](NamedTuple):
    root: Question[StudyProgrammeData]

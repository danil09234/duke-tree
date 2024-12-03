from typing import NamedTuple


class Question[StudyProgrammeData](NamedTuple):
    question: str
    yes_answer_node: "Question[StudyProgrammeData]" | StudyProgrammeData
    no_answer_node: "Question[StudyProgrammeData]" | StudyProgrammeData

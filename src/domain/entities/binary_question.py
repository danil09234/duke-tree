from typing import NamedTuple


class BinaryQuestion[StudyProgrammeData](NamedTuple):
    question: str
    yes_answer_node: "BinaryQuestion[StudyProgrammeData]" | StudyProgrammeData
    no_answer_node: "BinaryQuestion[StudyProgrammeData]" | StudyProgrammeData

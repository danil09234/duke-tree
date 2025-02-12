from typing import Optional, Union
from uuid import uuid4
from dataclasses import dataclass

from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.infrastructure.api.types.current_question_response import CurrentQuestionResponse
from src.interface_adapters.gateways.study_programmes_gateway_base import Page

QuestionNode = Union[
    OptionsQuestion[Page[ResTukeStudyProgrammeData]],
    BinaryQuestion[Page[ResTukeStudyProgrammeData]],
    Page[ResTukeStudyProgrammeData]
]


@dataclass
class SessionData:
    current_node: QuestionNode


class QuestionTreeAPISession:
    def __init__(self, decision_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
        self.decision_tree = decision_tree
        self.sessions: dict[str, SessionData] = {}

    def create_session(self) -> str:
        session_id = self._generate_session_id()
        self._initialize_session(session_id)
        return session_id

    def answer_question(self, session_id: str, answer: str) -> Optional[Page[ResTukeStudyProgrammeData]]:
        session = self._get_session(session_id)
        current_node = session.current_node

        if isinstance(current_node, OptionsQuestion):
            self._process_options_question(session, current_node, answer)
        elif isinstance(current_node, BinaryQuestion):
            self._process_binary_question(session, current_node, answer)
        else:
            raise ValueError("Decision tree has been completed")

        return self._finalize_session(session_id, session.current_node)

    def get_current_question(self, session_id: str) -> CurrentQuestionResponse:
        session = self._get_session(session_id)
        current_node = session.current_node

        if isinstance(current_node, OptionsQuestion):
            answers = [option.text for option in current_node.answer_options]
        elif isinstance(current_node, BinaryQuestion):
            answers = ["Yes", "No"]
        else:
            raise ValueError("No current question available")

        return CurrentQuestionResponse(
            question=current_node.text,
            answers=answers
        )

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid4())

    def _initialize_session(self, session_id: str) -> None:
        self.sessions[session_id] = SessionData(current_node=self.decision_tree.root)

    def _get_session(self, session_id: str) -> SessionData:
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
        return session

    @staticmethod
    def _process_options_question(session: SessionData, current_node: OptionsQuestion[Page[ResTukeStudyProgrammeData]], answer: str) -> None:
        option = next((opt for opt in current_node.answer_options if opt.text.lower() == answer.lower()), None)
        if not option:
            raise ValueError("Invalid answer option")
        session.current_node = option.answer_node

    @staticmethod
    def _process_binary_question(session: SessionData, current_node: BinaryQuestion[Page[ResTukeStudyProgrammeData]], answer: str) -> None:
        if answer.lower() == "yes":
            session.current_node = current_node.yes_answer_node
        elif answer.lower() == "no":
            session.current_node = current_node.no_answer_node
        else:
            raise ValueError("Answer must be 'yes' or 'no'")

    def _finalize_session(
            self,
            session_id: str,
            next_node: Union[QuestionNode, Page[ResTukeStudyProgrammeData]]
    ) -> Optional[Page[ResTukeStudyProgrammeData]]:
        if isinstance(next_node, Page):
            del self.sessions[session_id]
            return next_node
        return None

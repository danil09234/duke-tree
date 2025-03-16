from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.infrastructure.api.types.current_question_response import CurrentQuestionResponse
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.session_manager import SessionManager
from loguru import logger


class QuestionTreeAPI:
    def __init__(self, decision_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
        """
        Initialize the QuestionTreeAPI with a decision tree.

        :param decision_tree: The question tree to navigate
        """
        self._decision_tree = decision_tree
        self._session_manager = SessionManager(decision_tree)
        logger.info("Initialized QuestionTreeAPI")

    def create_session(self) -> str:
        """
        Create a new session and return its ID.

        :return: The unique session ID
        """
        session_id = self._session_manager.create_session()
        logger.info(f"Created new API session: {session_id}")
        return session_id

    def answer_question(self, session_id: str, answer: str) -> list[Page[ResTukeStudyProgrammeData]] | None:
        """
        Process an answer for the current question in a session.

        :param session_id: The ID of the session
        :param answer: The user's answer to the current question
        :return: List of study programs when the algorithm ends, otherwise None
        :raises SessionNotFoundError: If the session ID is not found
        """
        logger.debug(f"Processing answer for session {session_id}: {answer}")
        session = self._session_manager.get_session(session_id)
        return session.set_answer(answer)

    def get_current_question(self, session_id: str) -> CurrentQuestionResponse:
        """
        Retrieve the current question for a session.

        :param session_id: The ID of the session
        :return: The current question as a response object
        :raises SessionNotFoundError: If the session ID is not found
        """
        logger.debug(f"Getting current question for session {session_id}")
        session = self._session_manager.get_session(session_id)
        current_node = session.get_current_node()
        return current_node

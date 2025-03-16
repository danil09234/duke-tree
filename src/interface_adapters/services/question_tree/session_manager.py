from uuid import uuid4
from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.session import Session
from src.interface_adapters.services.question_tree.exceptions import SessionNotFoundError
from loguru import logger


class SessionManager:
    def __init__(self, decision_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
        """
        Initialize the SessionManager with a decision tree.

        :param decision_tree: The question tree to manage sessions for
        """
        self._sessions: dict[str, Session] = {}
        self._decision_tree = decision_tree
        logger.info("Initialized SessionManager")

    def create_session(self) -> str:
        """
        Create a new session.

        :return: The unique session ID
        """
        session_id = self._generate_session_id()
        session = Session(self._decision_tree.root)
        self._sessions[session_id] = session
        logger.info(f"Created new session with ID: {session_id}")
        return session_id

    def get_session(self, session_id: str) -> Session:
        """
        Retrieve a session by its ID.

        :param session_id: The ID of the session to retrieve
        :return: The session object
        :raises SessionNotFoundError: If the session ID does not exist
        """
        session = self._sessions.get(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            raise SessionNotFoundError(f"Session {session_id} not found")
        logger.debug(f"Retrieved session: {session_id}")
        return session

    @staticmethod
    def _generate_session_id() -> str:
        """
        Generate a unique session ID.

        :return: A new unique session identifier
        """
        return str(uuid4())
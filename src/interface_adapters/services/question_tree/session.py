from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.infrastructure.api.types.current_question_response import CurrentQuestionResponse
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.history_manager import HistoryManager
from src.interface_adapters.services.question_tree.question_mapping_manager import QuestionsMappingManager
from src.interface_adapters.services.question_tree.unvisited_queue import UnvisitedQueue
from src.interface_adapters.services.question_tree.type_aliases import TreeNode
from src.interface_adapters.services.question_tree.tree_iterator import TreeIterator
from loguru import logger


class Session:
    def __init__(self, root_node: TreeNode) -> None:
        """
        Initialize a new session with a root question node.

        :param root_node: The starting node of the question tree
        :raises RuntimeError: If root_node is a leaf node
        """
        logger.info("Initializing new session")
        self._history = HistoryManager()
        self._unvisited_queue = UnvisitedQueue()
        self._tree_mapping_manager = QuestionsMappingManager()
        self._iterator = TreeIterator(
            history=self._history,
            queue=self._unvisited_queue,
            tree_mapping_manager=self._tree_mapping_manager
        )
        self._iterator.start_with_node(root_node)
        logger.info("Session initialized successfully")

    def get_current_node(self) -> CurrentQuestionResponse:
        """
        Retrieve the current node for the session.

        :return: The current question node
        """
        return self._tree_mapping_manager.get_current_node()

    def set_answer(self, answer: str) -> list[Page[ResTukeStudyProgrammeData]] | None:
        """
        Set an answer to the current question and advance the session state.

        :param answer: The answer token
        :return: List of study programs if the algorithm ends, otherwise None
        """
        logger.debug(f"Setting answer: {answer}")
        return self._iterator.process_answer(answer)
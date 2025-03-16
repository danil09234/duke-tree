from typing import Optional
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.history_manager import HistoryManager
from src.interface_adapters.services.question_tree.unvisited_queue import UnvisitedQueue
from src.interface_adapters.services.question_tree.type_aliases import TreeNode
from src.interface_adapters.services.question_tree.type_aliases import QuestionNode
from src.interface_adapters.services.question_tree.question_mapping_manager import QuestionsMappingManager
from loguru import logger


class TreeIterator:
    def __init__(
        self,
        history: HistoryManager,
        queue: UnvisitedQueue,
        tree_mapping_manager: QuestionsMappingManager
    ) -> None:
        self._history = history
        self._unvisited_queue = queue
        self._tree_mapping_manager = tree_mapping_manager
        logger.debug("Initialized tree iterator")

    def _add_node_to_mapper(self, node: QuestionNode) -> None:
        node_id = self._tree_mapping_manager.add_node(node)
        if isinstance(node, OptionsQuestion):
            for answer_option in node.answer_options:
                self._tree_mapping_manager.add_answer_option(node_id, answer_option.text)
                logger.debug(f"Added answer option: {answer_option.text}")
        elif isinstance(node, BinaryQuestion):
            self._tree_mapping_manager.add_answer_option(node_id, "yes")
            self._tree_mapping_manager.add_answer_option(node_id, "no")
            self._tree_mapping_manager.add_answer_option(node_id, "probably")

    @staticmethod
    def _process_probably(answer_node: TreeNode) -> list[TreeNode]:
        logger.debug("Processing probably answer")
        if isinstance(answer_node, OptionsQuestion):
            return [option.answer_node for option in answer_node.answer_options]
        elif isinstance(answer_node, BinaryQuestion):
            return [answer_node.no_answer_node, answer_node.yes_answer_node]
        raise RuntimeError(f"Probably answer not valid for node type: {type(answer_node)}")

    @staticmethod
    def _process_standard_response(answer_node: TreeNode, answer_value: str) -> TreeNode:
        logger.debug(f"Processing standard answer: {answer_value}")
        if isinstance(answer_node, OptionsQuestion):
            for option in answer_node.answer_options:
                if option.text == answer_value:
                    return option.answer_node
            raise RuntimeError(f"Answer '{answer_value}' not found in answer options")
        elif isinstance(answer_node, BinaryQuestion):
            if answer_value == "yes":
                return answer_node.yes_answer_node
            elif answer_value == "no":
                return answer_node.no_answer_node
            raise RuntimeError(f"Answer '{answer_value}' not valid for binary question")
        raise RuntimeError(f"Answer node type not recognized: {type(answer_node)}")

    @classmethod
    def _process_answer_value(cls, answer_node: TreeNode, answer_value: str) -> list[TreeNode]:
        if answer_value == "probably":
            return cls._process_probably(answer_node)
        return [cls._process_standard_response(answer_node, answer_value)]

    def _get_next_nodes(self, answer_node: TreeNode, answer_token: str) -> list[TreeNode]:
        answer_value = self._tree_mapping_manager.get_answer_value_by_token(answer_token)
        logger.debug("Retrieved answer value: {}", answer_value)
        return self._process_answer_value(answer_node, answer_value)

    def _process_next_nodes(self, answer_node_id: int, answer_token: str) \
            -> Optional[list[Page[ResTukeStudyProgrammeData]]]:
        answer_node = self._tree_mapping_manager.get_node_by_id(answer_node_id)
        next_nodes = self._get_next_nodes(answer_node, answer_token)

        is_added_to_mapping = False

        for next_node in next_nodes:
            if isinstance(next_node, Page):
                self._history.add_entry(answer_node_id, next_node)
                logger.debug(f"Added study program from answer: {next_node.data.name}")
            elif isinstance(next_node, (BinaryQuestion, OptionsQuestion)):
                if not is_added_to_mapping:
                    self._add_node_to_mapper(next_node)
                    is_added_to_mapping = True
                    logger.debug("Added node to mapper")
                else:
                    self._unvisited_queue.add_node_to_visit(answer_node_id, next_node)
                    logger.debug("Added node to unvisited queue")

        if not is_added_to_mapping:
            logger.debug("Last leaf node reached in the current branch")
            if self._unvisited_queue.is_empty():
                logger.debug("Unvisited queue is empty")
                return self._history.get_results()
            else:
                logger.debug("Unvisited queue is not empty")
                queued_node = self._unvisited_queue.pop_next()
                if queued_node is None:
                    raise RuntimeError("Unvisited queue is not empty, but no nodes to visit")
                self._add_node_to_mapper(queued_node)
                logger.debug("Added node to mapper")
        return None

    def process_answer(self, answer_token: str) -> list[Page[ResTukeStudyProgrammeData]] | None:
        """
        Process a user's answer, handling answers to both current and past questions.

        :param answer_token: The answer token
        :return: List of study programs if the algorithm ends, otherwise None
        """
        logger.info(f"Processing answer token: {answer_token}")
        node_id = self._tree_mapping_manager.get_node_id_by_answer_token(answer_token)
        logger.debug(f"Answer token belongs to node: {node_id}")
        self._history.cancel_after_node(node_id)
        self._unvisited_queue.clear_from_key(node_id)
        self._tree_mapping_manager.clear_from_node_id(node_id)
        return self._process_next_nodes(node_id, answer_token)

    def start_with_node(self, root_node: TreeNode) -> None:
        if isinstance(root_node, Page):
            raise RuntimeError("Root node cannot be a leaf node")  # TODO: Review this
        self._add_node_to_mapper(root_node)

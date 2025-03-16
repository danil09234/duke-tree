from typing import NamedTuple
from uuid import uuid4
from collections import OrderedDict
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.binary_question import BinaryQuestion
from src.infrastructure.api.types.current_question_response import CurrentQuestionResponse
from src.interface_adapters.services.question_tree.exceptions import AnswerTokenNotFound
from src.interface_adapters.services.question_tree.type_aliases import QuestionNode


class AnswerWrapper(NamedTuple):
    value: str
    node: int


class QuestionsMappingManager:
    """
    Manages the mapping between questions, their IDs, and answer options.

    Provides functionality for tracking question nodes and their associated
    answer options, generating unique tokens for answers.
    """

    def __init__(self) -> None:
        self._question_nodes_mapping: dict[int, QuestionNode] = {}
        self._answer_tokens_mapping: OrderedDict[str, AnswerWrapper] = OrderedDict()
        self._counter = 0

    def add_node(self, node: QuestionNode) -> int:
        """
        Add a new question node to the mapping.

        :param node: The question node to add
        :return: The assigned node ID
        """
        node_id = self._generate_node_id()
        self._store_node(node_id, node)
        return node_id

    def add_answer_option(self, node_id: int, value: str) -> str:
        """
        Add an answer option for a question node.

        :param node_id: The ID of the question node
        :param value: The value of the answer option
        :return: Generated unique token for the answer
        """
        answer_token = self._generate_answer_token()
        self._answer_tokens_mapping[answer_token] = AnswerWrapper(value=value, node=node_id)
        return answer_token

    def get_node_id_by_answer_token(self, answer_token: str) -> int:
        """
        Get the node ID associated with an answer token.

        :param answer_token: The answer token to look up
        :return: The ID of the node that has this answer
        :raises AnswerTokenNotFound: If answer token is not found
        """
        try:
            return self._answer_tokens_mapping[answer_token].node
        except KeyError:
            raise AnswerTokenNotFound()

    def get_node_by_id(self, node_id: int) -> QuestionNode:
        """
        Retrieve a node by its ID.

        :param node_id: The ID of the node to retrieve
        :return: The corresponding tree node
        :raises KeyError: If node ID is not found
        """
        return self._question_nodes_mapping[node_id]

    def get_answer_value_by_token(self, answer_token: str) -> str:
        """
        Get the answer value associated with a token.

        :param answer_token: The token to look up
        :return: The corresponding answer value
        :raises KeyError: If token is not found
        """
        return self._answer_tokens_mapping[answer_token].value

    def _generate_node_id(self) -> int:
        self._counter += 1
        return self._counter

    @staticmethod
    def _generate_answer_token() -> str:
        return str(uuid4())

    def _store_node(self, node_id: int, node: QuestionNode) -> None:
        self._question_nodes_mapping[node_id] = node

    def get_last_node_id(self) -> int:
        return int(list(self._question_nodes_mapping.keys())[-1])

    def get_current_node(self) -> CurrentQuestionResponse:
        return self._wrap_node(self.get_last_node_id())

    def _wrap_node(self, node_id: int) -> CurrentQuestionResponse:
        node = self._question_nodes_mapping[node_id]
        if isinstance(node, OptionsQuestion):
            question = node.text
        elif isinstance(node, BinaryQuestion):
            question = node.text
        else:
            raise TypeError(f"Invalid node type: {type(node_id)}")

        answer_options: dict[str, str] = {}

        for answer_token, wrapper in self._answer_tokens_mapping.items():
            if wrapper.node == node_id:
                answer_options[answer_token] = wrapper.value

        return CurrentQuestionResponse(
            question=question,
            answers=answer_options
        )

    def clear_from_node_id(self, node_id: int) -> None:
        """
        Clear all mappings after the specified node ID.

        :param node_id: The node ID after which to clear mappings
        """
        self._clear_answer_tokens_mapping(node_id)
        self._clear_question_nodes_mapping(node_id)
        self._counter = node_id

    def _clear_question_nodes_mapping(self, node_id: int) -> None:
        keys = list(self._question_nodes_mapping.keys())
        for key in keys:
            if key > node_id:
                del self._question_nodes_mapping[key]

    def _clear_answer_tokens_mapping(self, node_id: int) -> None:
        keys = list(self._answer_tokens_mapping.keys())
        for key in keys:
            if self._answer_tokens_mapping[key].node > node_id:
                del self._answer_tokens_mapping[key]

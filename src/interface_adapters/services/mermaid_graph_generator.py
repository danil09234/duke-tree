from typing import override

from src.application.interfaces import QuestionTreeGraphGenerator
from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page

type Node = (
        OptionsQuestion[Page[ResTukeStudyProgrammeData]]
        | BinaryQuestion[Page[ResTukeStudyProgrammeData]]
        | Page[ResTukeStudyProgrammeData]
)


class MermaidGraphGenerator(QuestionTreeGraphGenerator[Page[ResTukeStudyProgrammeData]]):
    def __init__(self) -> None:
        self._lines: list[str] = []
        self._id_counter = 0
        self._visited_nodes: dict[int, str] = {}

    @override
    def generate(self, question_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> str:
        self._initialize_graph()
        root_id = self._create_node_id()
        self._process_node(question_tree.root, root_id)
        return "\n\t".join(self._lines)

    def _initialize_graph(self) -> None:
        self._lines.clear()
        self._lines.append("graph TD")
        self._id_counter = 0
        self._visited_nodes.clear()

    def _create_node_id(self) -> str:
        node_id = f"n{self._id_counter}"
        self._id_counter += 1
        return node_id

    def _process_node(self, node: Node, node_id: str) -> None:
        self._add_node(node, node_id)
        self._mark_as_visited(node, node_id)
        self._handle_transitions(node, node_id)

    def _add_node(self, node: Node, node_id: str) -> None:
        label = self._get_label(node)
        self._lines.append(f'{node_id}["{label}"]')

    def _mark_as_visited(self, node: Node, node_id: str) -> None:
        self._visited_nodes[id(node)] = node_id

    def _handle_transitions(self, node: Node, parent_id: str) -> None:
        if isinstance(node, OptionsQuestion):
            self._handle_options_transitions(node, parent_id)
        elif isinstance(node, BinaryQuestion):
            self._handle_binary_transitions(node, parent_id)

    @staticmethod
    def _get_label(node: Node) -> str:
        if isinstance(node, (OptionsQuestion, BinaryQuestion)):
            return node.text
        elif isinstance(node, Page) and isinstance(node.data, ResTukeStudyProgrammeData):
            return node.data.name
        return "Unknown"

    def _handle_options_transitions(
            self, node: OptionsQuestion[Page[ResTukeStudyProgrammeData]], parent_id: str
    ) -> None:
        for option in node.answer_options:
            child_id = self._get_existing_node_id(option.answer_node)
            self._add_transition(parent_id, option.text, child_id)
            self._process_node(option.answer_node, child_id)

    def _handle_binary_transitions(
            self, node: BinaryQuestion[Page[ResTukeStudyProgrammeData]], parent_id: str
    ) -> None:
        yes_id = self._get_existing_node_id(node.yes_answer_node)
        no_id = self._get_existing_node_id(node.no_answer_node)
        self._add_transition(parent_id, "Yes", yes_id)
        self._add_transition(parent_id, "No", no_id)
        self._process_node(node.yes_answer_node, yes_id)
        self._process_node(node.no_answer_node, no_id)

    def _add_transition(self, parent_id: str, label: str, child_id: str) -> None:
        self._lines.append(f'{parent_id} -->|{label}| {child_id}')

    def _get_existing_node_id(self, node: object) -> str:
        return self._visited_nodes.get(id(node), self._create_node_id())

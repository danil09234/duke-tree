from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.question_tree import QuestionsTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page

type Node = (
        OptionsQuestion[Page[ResTukeStudyProgrammeData]]
        | BinaryQuestion[Page[ResTukeStudyProgrammeData]]
        | Page[ResTukeStudyProgrammeData]
)


class MermaidGraphGenerator:
    def __init__(self) -> None:
        self._lines: list[str] = []
        self._id_counter = 0
        self._visited: dict[int, str] = {}

    def generate_code(self, questions_tree: QuestionsTree[Page[ResTukeStudyProgrammeData]]) -> str:
        self._reset_graph()
        root_id = self._get_node_id()
        self._visit_node(questions_tree.root, root_id)
        return "\n\t".join(self._lines)

    def _reset_graph(self) -> None:
        self._lines.clear()
        self._lines.append("graph TD")
        self._id_counter = 0
        self._visited.clear()

    def _visit_node(self, node: Node, node_id: str) -> None:
        self._add_node_line(node, node_id)
        self._mark_node_visited(node, node_id)
        self._handle_node_transitions(node, node_id)

    def _add_node_line(self, node: Node, node_id: str) -> None:
        node_label = self._get_node_label(node)
        self._lines.append(f'{node_id}["{node_label}"]')

    def _mark_node_visited(self, node: Node, node_id: str) -> None:
        self._visited[id(node)] = node_id

    def _handle_node_transitions(self, node: Node, node_id: str) -> None:
        if isinstance(node, OptionsQuestion):
            self._handle_options_question_transitions(node, node_id)
        elif isinstance(node, BinaryQuestion):
            self._handle_binary_question_transitions(node, node_id)

    @staticmethod
    def _get_node_label(node: Node) -> str:
        if isinstance(node, OptionsQuestion):
            return node.text
        elif isinstance(node, BinaryQuestion):
            return node.text
        elif isinstance(node, Page) and isinstance(node.data, ResTukeStudyProgrammeData):
            return node.data.name
        else:
            return "Unknown"

    def _handle_options_question_transitions(
            self, node: OptionsQuestion[Page[ResTukeStudyProgrammeData]], parent_id: str
    ) -> None:
        for option in node.answer_options:
            child_id = self._get_or_create_node_id(option.answer_node)
            self._add_transition_line(parent_id, option.text, child_id)
            self._visit_node(option.answer_node, child_id)

    def _handle_binary_question_transitions(
            self, node: BinaryQuestion[Page[ResTukeStudyProgrammeData]], parent_id: str
    ) -> None:
        yes_id = self._get_or_create_node_id(node.yes_answer_node)
        no_id = self._get_or_create_node_id(node.no_answer_node)
        self._add_transition_line(parent_id, "Yes", yes_id)
        self._add_transition_line(parent_id, "No", no_id)
        self._visit_node(node.yes_answer_node, yes_id)
        self._visit_node(node.no_answer_node, no_id)

    def _add_transition_line(self, parent_id: str, label: str, child_id: str) -> None:
        self._lines.append(f'{parent_id} -->|{label}| {child_id}')

    def _get_or_create_node_id(self, node: object) -> str:
        if id(node) in self._visited:
            return self._visited[id(node)]
        return self._get_node_id()

    def _get_node_id(self) -> str:
        node_id = f"n{self._id_counter}"
        self._id_counter += 1
        return node_id

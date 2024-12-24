from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.mermaid_graph_generator import MermaidGraphGenerator
from src.domain.entities.question_tree import QuestionsTree


def test_generate_graph_simple(simple_binary_tree: QuestionsTree[Page[ResTukeStudyProgrammeData]]) -> None:
    generator = MermaidGraphGenerator()
    graph = generator.generate(simple_binary_tree)
    expected_graph = (
        "graph TD\n\t"
        'n0["Are you interested in computer technologies?"]\n\t'
        'n0 -->|Yes| n1\n\t'
        'n0 -->|No| n2\n\t'
        'n1["Programme 1 EN"]\n\t'
        'n2["Programme 2 EN"]'
    )
    assert graph == expected_graph


def test_generate_graph_complex(complex_tree: QuestionsTree[Page[ResTukeStudyProgrammeData]]) -> None:
    generator = MermaidGraphGenerator()
    graph = generator.generate(complex_tree)
    expected_graph = (
        "graph TD\n\t"
        'n0["Are you interested in computer technologies?"]\n\t'
        'n0 -->|Yes| n1\n\t'
        'n0 -->|No| n2\n\t'
        'n1["Programme 1 EN"]\n\t'
        'n2["Are you interested in quality management?"]\n\t'
        'n2 -->|Yes| n3\n\t'
        'n2 -->|No| n4\n\t'
        'n3["Programme 3 EN"]\n\t'
        'n4["Programme 2 EN"]'
    )
    assert graph == expected_graph


def test_handle_options_transitions(options_transitions_tree: QuestionsTree[Page[ResTukeStudyProgrammeData]]) -> None:
    generator = MermaidGraphGenerator()
    graph = generator.generate(options_transitions_tree)
    expected_graph = (
        "graph TD\n\t"
        'n0["Do you like programming?"]\n\t'
        'n0 -->|Yes| n1\n\t'
        'n1["Programme 1 EN"]\n\t'
        'n0 -->|No| n2\n\t'
        'n2["Programme 2 EN"]'
    )
    assert graph == expected_graph


def test_full_generation(full_generation_tree: QuestionsTree[Page[ResTukeStudyProgrammeData]]) -> None:
    generator = MermaidGraphGenerator()
    graph = generator.generate(full_generation_tree)
    expected_graph = (
        "graph TD\n\t"
        'n0["Do you prefer theoretical or practical learning?"]\n\t'
        'n0 -->|Theoretical| n1\n\t'
        'n1["Programme 1 SK"]\n\t'
        'n0 -->|Practical| n2\n\t'
        'n2["Are you interested in computer technologies?"]\n\t'
        'n2 -->|Yes| n3\n\t'
        'n2 -->|No| n4\n\t'
        'n3["Programme 1 EN"]\n\t'
        'n4["Are you interested in quality management?"]\n\t'
        'n4 -->|Yes| n5\n\t'
        'n4 -->|No| n6\n\t'
        'n5["Programme 3 EN"]\n\t'
        'n6["Programme 2 EN"]'
    )
    assert graph == expected_graph

import pytest

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion, AnswerOption
from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession


@pytest.fixture(scope="function")
def api_session(request: pytest.FixtureRequest) -> QuestionTreeAPISession:
    fixture_name = request.param
    tree = request.getfixturevalue(fixture_name)
    return QuestionTreeAPISession(tree)


@pytest.fixture
def simple_binary_tree(test_study_programmes: list[Page[ResTukeStudyProgrammeData]]) \
        -> QuestionTree[Page[ResTukeStudyProgrammeData]]:
    programme1 = test_study_programmes[0]
    programme2 = test_study_programmes[1]

    binary_question = BinaryQuestion(
        text="Are you interested in computer technologies?",
        yes_answer_node=programme1,
        no_answer_node=programme2
    )

    question_tree: QuestionTree[Page[ResTukeStudyProgrammeData]] = QuestionTree(root=binary_question)
    return question_tree


@pytest.fixture
def complex_tree(test_study_programmes: list[Page[ResTukeStudyProgrammeData]]) \
        -> QuestionTree[Page[ResTukeStudyProgrammeData]]:
    programme1 = test_study_programmes[0]
    programme2 = test_study_programmes[1]
    programme3 = test_study_programmes[2]

    binary_q2 = BinaryQuestion(
        text="Are you interested in quality management?",
        yes_answer_node=programme3,
        no_answer_node=programme2
    )

    binary_q1 = BinaryQuestion(
        text="Are you interested in computer technologies?",
        yes_answer_node=programme1,
        no_answer_node=binary_q2
    )

    question_tree: QuestionTree[Page[ResTukeStudyProgrammeData]] = QuestionTree(root=binary_q1)
    return question_tree


@pytest.fixture
def options_transitions_tree(test_study_programmes: list[Page[ResTukeStudyProgrammeData]]) \
        -> QuestionTree[Page[ResTukeStudyProgrammeData]]:
    programme_yes = test_study_programmes[0]
    programme_no = test_study_programmes[1]

    option1 = AnswerOption(text="Yes", answer_node=programme_yes)
    option2 = AnswerOption(text="No", answer_node=programme_no)

    options_question = OptionsQuestion(
        text="Do you like programming?",
        answer_options=[option1, option2]
    )

    return QuestionTree(root=options_question)


@pytest.fixture
def full_generation_tree(test_study_programmes: list[Page[ResTukeStudyProgrammeData]]) \
        -> QuestionTree[Page[ResTukeStudyProgrammeData]]:
    programme1 = test_study_programmes[0]
    programme2 = test_study_programmes[1]
    programme3 = test_study_programmes[2]
    programme4 = test_study_programmes[3]

    binary_q2 = BinaryQuestion(
        text="Are you interested in quality management?",
        yes_answer_node=programme3,
        no_answer_node=programme2
    )

    binary_q1 = BinaryQuestion(
        text="Are you interested in computer technologies?",
        yes_answer_node=programme1,
        no_answer_node=binary_q2
    )

    option1: AnswerOption[Page[ResTukeStudyProgrammeData]] = AnswerOption(text="Theoretical", answer_node=programme4)
    option2: AnswerOption[Page[ResTukeStudyProgrammeData]] = (
        AnswerOption(text="Practical", answer_node=binary_q1)
    )

    options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]] = OptionsQuestion(
        text="Do you prefer theoretical or practical learning?",
        answer_options=[option1, option2]
    )

    return QuestionTree(root=options_question)

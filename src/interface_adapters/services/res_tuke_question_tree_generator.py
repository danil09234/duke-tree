from src.application.interfaces import QuestionTreeGenerator, LLMDecisionTreeQuestionGenerator
from src.domain.entities.question_tree import QuestionsTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question import Question
from src.interface_adapters.gateways.study_programmes_gateway_base import Page


class ResTukeQuestionTreeGenerator(QuestionTreeGenerator[Page[ResTukeStudyProgrammeData]]):
    def __init__(
            self,
            llm_decision_tree_question_generator_service: LLMDecisionTreeQuestionGenerator[
                Page[ResTukeStudyProgrammeData]
            ]
    ) -> None:
        self._llm_decision_tree_question_generator_service = llm_decision_tree_question_generator_service

    async def generate(
            self,
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> QuestionsTree[Page[ResTukeStudyProgrammeData]]:
        root_question = await self._generate_node(study_programmes)
        return QuestionsTree(root=root_question)

    async def _generate_node(
            self,
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> Question[Page[ResTukeStudyProgrammeData]] | Page[ResTukeStudyProgrammeData]:
        if self._is_single_programme(study_programmes):
            return study_programmes[0]

        question = await self._llm_decision_tree_question_generator_service.generate_question(study_programmes)

        yes_programmes = self._filter_programmes(study_programmes, question.yes_nodes)
        no_programmes = self._filter_programmes(study_programmes, question.no_nodes)

        yes_node = await self._generate_node(yes_programmes)
        no_node = await self._generate_node(no_programmes)

        return self._create_question(question.text, yes_node, no_node)

    @staticmethod
    def _is_single_programme(study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> bool:
        return len(study_programmes) == 1

    @staticmethod
    def _create_question(
            question_text: str,
            yes_node: Question[Page[ResTukeStudyProgrammeData]] | Page[ResTukeStudyProgrammeData],
            no_node: Question[Page[ResTukeStudyProgrammeData]] | Page[ResTukeStudyProgrammeData]
    ) -> Question[Page[ResTukeStudyProgrammeData]]:
        return Question(
            question=question_text,
            yes_answer_node=yes_node,
            no_answer_node=no_node,
        )

    @staticmethod
    def _filter_programmes(
            study_programmes: list[Page[ResTukeStudyProgrammeData]],
            codes_list: list[str]
    ) -> list[Page[ResTukeStudyProgrammeData]]:
        return [study_programme for study_programme in study_programmes if study_programme.metadata.code in codes_list]

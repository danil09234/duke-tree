from typing import Callable, Any, Awaitable, Union

from loguru import logger

from src.application.interfaces import QuestionTreeGenerator, LLMDecisionTreeQuestionGenerator
from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion, AnswerOption
from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
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
    ) -> QuestionTree[Page[ResTukeStudyProgrammeData]]:
        root_question = await self._generate_preferred_language_question(study_programmes)
        return QuestionTree(root=root_question)

    async def _generate_preferred_language_question(
            self, 
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> OptionsQuestion[Page[ResTukeStudyProgrammeData]]:
        logger.debug("Generating preferred language question")
        return await self._generate_options_question(
            "What is your preferred language?",
            study_programmes,
            lambda x: x.metadata.language,
            self._generate_level_of_degree_question
        )

    async def _generate_level_of_degree_question(
            self, 
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> OptionsQuestion[Page[ResTukeStudyProgrammeData]]:
        logger.debug("Generating level of degree question")
        return await self._generate_options_question(
            "What level of degree are you interested in?",
            study_programmes,
            lambda x: x.data.level_of_degree,
            self._generate_study_form_question
        )

    async def _generate_study_form_question(
            self, 
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> OptionsQuestion[Page[ResTukeStudyProgrammeData]]:
        logger.debug("Generating study form question")
        return await self._generate_options_question(
            "What study form are you interested in?",
            study_programmes,
            lambda x: x.data.study_form,
            self._generate_binary_node
        )

    @staticmethod
    async def _generate_options_question(
        question_text: str,
        study_programmes: list[Page[ResTukeStudyProgrammeData]],
        get_property: Callable[[Page[ResTukeStudyProgrammeData]], Any],
        next_step: Callable[
            [list[Page[ResTukeStudyProgrammeData]]],
            Awaitable[
                Union[
                    BinaryQuestion[Page[ResTukeStudyProgrammeData]],
                    OptionsQuestion[Page[ResTukeStudyProgrammeData]],
                    Page[ResTukeStudyProgrammeData]
                ]
            ]
        ]
    ) -> OptionsQuestion[Page[ResTukeStudyProgrammeData]]:
        distinct_values = {get_property(study_programme) for study_programme in study_programmes}
        answer_options = []
        for value in distinct_values:
            filtered = [
                study_programme for study_programme in study_programmes if get_property(study_programme) == value
            ]
            answer_node = await next_step(filtered)
            answer_options.append(AnswerOption(text=str(value), answer_node=answer_node))

        return OptionsQuestion(text=question_text, answer_options=answer_options)

    async def _generate_binary_node(
            self,
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> Union[BinaryQuestion[Page[ResTukeStudyProgrammeData]], Page[ResTukeStudyProgrammeData]]:
        if self._is_single_programme(study_programmes):
            return study_programmes[0]

        question = await self._llm_decision_tree_question_generator_service.generate_question(study_programmes)

        yes_programmes = self._filter_programmes(study_programmes, question.yes_nodes)
        no_programmes = self._filter_programmes(study_programmes, question.no_nodes)

        yes_node = await self._generate_binary_node(yes_programmes)
        no_node = await self._generate_binary_node(no_programmes)

        return BinaryQuestion(
            text=question.text,
            yes_answer_node=yes_node,
            no_answer_node=no_node,
        )

    @staticmethod
    def _is_single_programme(study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> bool:
        return len(study_programmes) == 1

    @staticmethod
    def _filter_programmes(
            study_programmes: list[Page[ResTukeStudyProgrammeData]],
            codes_list: list[str]
    ) -> list[Page[ResTukeStudyProgrammeData]]:
        return [study_programme for study_programme in study_programmes if study_programme.metadata.code in codes_list]

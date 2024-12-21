from openai import AsyncOpenAI
from typing import Any
import json

from src.application.interfaces import QuestionTreeGenerator
from src.domain.entities.question_tree import QuestionsTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question import Question
from src.interface_adapters.gateways.study_programmes_gateway_base import Page


class ResTukeQuestionTreeGenerator(QuestionTreeGenerator[Page[ResTukeStudyProgrammeData]]):
    def __init__(self, api_key: str):
        self._api_key = api_key

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

        response = await self._get_response(study_programmes)
        question_text, yes_codes, no_codes = self._extract_response_data(response)

        yes_programmes = self._filter_programmes(study_programmes, yes_codes)
        no_programmes = self._filter_programmes(study_programmes, no_codes)

        yes_node = await self._generate_node(yes_programmes)
        no_node = await self._generate_node(no_programmes)

        return self._create_question(question_text, yes_node, no_node)

    @staticmethod
    def _is_single_programme(study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> bool:
        return len(study_programmes) == 1

    async def _get_response(
            self,
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> dict[str, Any]:
        return await self._call_openai_api(study_programmes)

    @staticmethod
    def _extract_response_data(response: dict[str, Any]) -> tuple[str, list[str], list[str]]:
        return response['question'], response['yes'], response['no']

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

    async def _call_openai_api(
        self,
        study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> dict[str, Any]:
        client = AsyncOpenAI(
            api_key=self._api_key,
        )
        user_message = self._create_user_message(study_programmes)

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "text": "You are an AI assistant tasked wth designing a binary decision tree to recommend "
                                    "university study programmes at TUKE. Each study programme is represented by its "
                                    "'code' and attributes provided in JSON format. Your goal is to generate a yes/no "
                                    "question for the university applicant that divides the programmes into two "
                                    "meaningful groups ('yes' and 'no') based on their attributes.\n\nProvide the "
                                    "output in the following JSON schema:\n\n```\n{\n  \"question\": "
                                    "\"Your question here\",\n  \"yes\": [\"List of study programme codes that answer "
                                    "'yes'\"],\n  \"no\": [\"List of study programme codes that answer 'no'\"]\n}\n"
                                    "```\n\n**Rules:**\n\n1. Your question **must result in both 'yes' and 'no' groups "
                                    "containing at least one programme**. Questions that produce empty groups are "
                                    "invalid and should not be proposed.\n2. Ensure the division is meaningful and "
                                    "based on the attributes provided, avoiding trivial or overly specific splits.\n3. "
                                    "Consider attributes like study field, level of degree, study form, length of "
                                    "study, and others when formulating questions. The split should help refine the "
                                    "decision tree by grouping similar programmes.\n4. Use only the provided "
                                    "attributes for generating questions, and ensure the question aligns logically "
                                    "with these attributes.\n5. All paths in the decision tree must eventually cover "
                                    "all available study programmes, with no redundancy between paths.\n\nAttributes "
                                    "of each study programme:\n\n- `code`: str (Unique identifier for each programme)\n"
                                    "- `study_field`: str\n- `level_of_degree`: int\n- `study_form`: str\n- `degree`: "
                                    "str\n- `length_of_study_in_years`: int\n- `professionally_oriented`: bool\n- "
                                    "`joint_study_program`: bool\n- `languages_of_delivery`: str\n- `description`: "
                                    "str\n- `learning_objectives`: str\n- `main_learning_outcomes`: str\n- `faculty`: "
                                    "str\n\n**Important:** Before proposing a question, simulate its application to "
                                    "the given list of programmes. If the split results in an empty 'yes' or 'no' "
                                    "group, refine your question or select a different attribute to base the split on. "
                                    "Every question must meaningfully divide the programmes. Remember: Your questions "
                                    "will be displayed to the applicant and must ask about the applicants interests if "
                                    "possible. Questions must not contain too complex terms for the applicant, "
                                    "everything has to be clear for him. You have to include all study programmes in "
                                    "your response, this is very important.",
                            "type": "text"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message
                        }
                    ]
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "binary_decision_tree",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The yes/no question to ask a university applicant to divide the study "
                                               "programmes into two groups."
                            },
                            "yes": {
                                "type": "array",
                                "description": "List of study programme codes that answer 'yes'.",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "no": {
                                "type": "array",
                                "description": "List of study programme codes that answer 'no'.",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "required": [
                            "question",
                            "yes",
                            "no"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_json = response.choices[0].message.content

        if response_json is None:
            raise RuntimeError

        return self._parse_model_response(response_json)

    @staticmethod
    def _create_user_message(
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> str:
        programmes_data = []

        for programme_data in study_programmes:
            programmes_data.append({
                "code": programme_data.metadata.code,
                "study_field": programme_data.data.study_field,
                "level_of_degree": programme_data.data.level_of_degree,
                "study_form": programme_data.data.study_form,
                "degree": programme_data.data.degree,
                "length_of_study_in_years": programme_data.data.length_of_study_in_years,
                "professionally_oriented": programme_data.data.professionally_oriented,
                "joint_study_program": programme_data.data.joint_study_program,
                "languages_of_delivery": programme_data.data.languages_of_delivery,
                "description": programme_data.data.description,
                "learning_objectives": programme_data.data.learning_objectives,
            })

        message = (
            "Here is the list of study programmes:\n"
            f"{programmes_data}\n\nPlease generate a question as per the instructions."
        )
        return message

    @staticmethod
    def _parse_model_response(content: str) -> dict[str, Any]:
        try:
            return dict(json.loads(content))
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON response from the model.") from e

    @staticmethod
    def _filter_programmes(
            study_programmes: list[Page[ResTukeStudyProgrammeData]],
            codes_list: list[str]
    ) -> list[Page[ResTukeStudyProgrammeData]]:
        return [study_programme for study_programme in study_programmes if study_programme.metadata.code in codes_list]

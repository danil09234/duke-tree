import json
from typing import Union, Any

from loguru import logger
from openai import AsyncOpenAI
from openai.types import ChatModel

from src.application.interfaces import LLMDecisionTreeQuestionGenerator
from src.domain.dtos.decision_tree_question import DecisionTreeQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page


class OpenAIDecisionTreeQuestionGenerator(
    LLMDecisionTreeQuestionGenerator[Page[ResTukeStudyProgrammeData]]
):
    _system_prompt = (
        "You are an AI assistant tasked with designing a binary decision tree to recommend "
        "university study programmes at TUKE. Each study programme is represented by its "
        "'code' and attributes provided in JSON format. Your goal is to generate a yes/no "
        "question for the university applicant that divides the programmes into two "
        "meaningful (and not empty!) groups ('yes' and 'no') based on their attributes.\n\n"
        "Provide the output in the following JSON schema:\n\n"
        "```\n"
        "{\n"
        '  "question": "Your question here",\n'
        '  "yes": ["List of study programme codes answering \'yes\'"],\n'
        '  "no": ["List of study programme codes answering \'no\'"]\n'
        "}\n"
        "```\n\n"
        "**Rules:**\n\n"
        "1. Your question must result in both 'yes' and 'no' groups containing at least one programme. Important!\n"
        "2. Ensure the division is meaningful and based on the attributes provided, avoiding trivial or overly "
        "specific splits.\n"
        "3. Use only the provided attributes for generating questions, and ensure the question aligns logically "
        "with these attributes.\n"
        "4. All paths in the decision tree must eventually cover all available study programmes, with no "
        "redundancy.\n\n"
        "Attributes:\n"
        "- `code`: str\n"
        "- `study_field`: str\n"
        "- `description`: str\n"
        "- `learning_objectives`: str\n"
        "Before proposing the question, simulate its effect on the given programmes so neither 'yes' nor 'no' "
        "group is empty. "
        "Ask about the applicants' interests, not about the programmes themselves. Keep the question accessible "
        "and clear. All initial programmes must appear in the returned results - this is very important."
    )

    _response_schema = {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The yes/no question that divides the study programmes into two groups."
            },
            "yes": {
                "type": "array",
                "description": "Not empty list of study programme codes that answer 'yes'.",
                "items": {
                    "type": "string"
                }
            },
            "no": {
                "type": "array",
                "description": "Not empty list of study programme codes that answer 'no'.",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["question", "yes", "no"],
        "additionalProperties": False
    }

    def __init__(
            self,
            api_key: str,
            model: Union[str, ChatModel] = "gpt-4o",
            temperature: float = 1.0,
            max_tokens: int = 2048,
            top_p: float = 1.0,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._top_p = top_p
        self._frequency_penalty = frequency_penalty
        self._presence_penalty = presence_penalty

    async def generate_question(
            self,
            study_programmes: list[Page[ResTukeStudyProgrammeData]]
    ) -> DecisionTreeQuestion:
        client = AsyncOpenAI(api_key=self._api_key)
        user_message = self._create_user_message(study_programmes)

        response = await client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": [{"text": self._system_prompt, "type": "text"}]},
                {"role": "user", "content": [{"text": user_message, "type": "text"}]},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "binary_decision_tree_question",
                    "strict": True,
                    "schema": self._response_schema
                }
            },
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p,
            frequency_penalty=self._frequency_penalty,
            presence_penalty=self._presence_penalty,
        )

        response_json = response.choices[0].message.content
        if response_json is None:
            raise RuntimeError("No JSON content returned from the language model API.")
        parsed_response = self._parse_model_response(response_json)
        logger.debug(f"Generated question: {parsed_response}")
        return DecisionTreeQuestion(
            text=parsed_response["question"],
            yes_nodes=parsed_response["yes"],
            no_nodes=parsed_response["no"]
        )

    @staticmethod
    def _create_user_message(study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> str:
        programme_data = []

        for programme in study_programmes:
            programme_data.append({
                "code": programme.metadata.code,
                "study_field": programme.data.study_field,
                "description": programme.data.description,
                "learning_objectives": programme.data.learning_objectives,
            })
        return (
            "Here is the list of study programmes:\n"
            f"{programme_data}\n\n"
            "Please generate a question as per the instructions."
        )

    @staticmethod
    def _parse_model_response(content: str) -> dict[str, Any]:
        try:
            return dict(json.loads(content))
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON response from language model.") from e

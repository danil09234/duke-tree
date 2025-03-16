from src.interface_adapters.services.question_tree.api import QuestionTreeAPI
from src.infrastructure.api.dependencies.singleton_question_tree_api_session import SingletonQuestionTreeAPI


async def get_question_tree_api() -> QuestionTreeAPI:
    return await SingletonQuestionTreeAPI.get_instance()

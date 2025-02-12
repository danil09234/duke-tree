from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession
from src.infrastructure.api.dependencies.singleton_question_tree_api_session import SingletonQuestionTreeAPISession


async def get_question_tree_api_session() -> QuestionTreeAPISession:
    return await SingletonQuestionTreeAPISession.get_instance()

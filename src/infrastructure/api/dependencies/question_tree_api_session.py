from src.interface_adapters.persistence.serializer_storage import SerializerStorage
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question_tree import QuestionTree


async def get_question_tree_api_session() -> QuestionTreeAPISession:
    serializer_storage = SerializerStorage[QuestionTree[Page[ResTukeStudyProgrammeData]]]("/app/data/questions-tree.pkl")
    question_tree: QuestionTree[Page[ResTukeStudyProgrammeData]] = (await serializer_storage.get_all())[0]
    return QuestionTreeAPISession(question_tree)

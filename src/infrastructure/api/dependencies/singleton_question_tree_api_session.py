from threading import Lock
from typing import Optional, TypeVar, Generic
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession
from src.interface_adapters.persistence.serializer_storage import SerializerStorage
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question_tree import QuestionTree


T = TypeVar('T')


class SingletonQuestionTreeAPISession:
    _instance: Optional[QuestionTreeAPISession] = None
    _lock = Lock()

    @classmethod
    async def get_instance(cls) -> QuestionTreeAPISession:
        with cls._lock:
            if cls._instance is None:
                serializer_storage = SerializerStorage[QuestionTree[Page[ResTukeStudyProgrammeData]]]("/app/data/questions-tree.pkl")
                question_tree = (await serializer_storage.get_all())[0]
                cls._instance = QuestionTreeAPISession(question_tree)
        return cls._instance
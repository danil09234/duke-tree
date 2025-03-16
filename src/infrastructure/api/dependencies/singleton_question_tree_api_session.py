from threading import Lock
from typing import Optional
from src.interface_adapters.services.question_tree.api import QuestionTreeAPI
from src.interface_adapters.persistence.serializer_storage import SerializerStorage
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question_tree import QuestionTree


class SingletonQuestionTreeAPI:
    _instance: Optional[QuestionTreeAPI] = None
    _lock = Lock()

    @classmethod
    async def get_instance(cls) -> QuestionTreeAPI:
        with cls._lock:
            if cls._instance is None:
                serializer_storage = SerializerStorage[QuestionTree[Page[ResTukeStudyProgrammeData]]]("/app/data/questions-tree.pkl")
                question_tree = (await serializer_storage.get_all())[0]
                cls._instance = QuestionTreeAPI(question_tree)
        return cls._instance
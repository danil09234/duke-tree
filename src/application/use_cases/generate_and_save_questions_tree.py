from src.application.interfaces import QuestionTreeGenerator
from src.domain.entities.question_tree import QuestionTree
from src.application.interfaces import Savable, GetAllRepository


class GenerateAndSaveQuestionsTreeUseCase[StudyProgrammeData]:
    def __init__(
            self,
            study_programmes_repository: GetAllRepository[StudyProgrammeData],
            questions_tree_generator: QuestionTreeGenerator[StudyProgrammeData],
            question_tree_storage: Savable[QuestionTree[StudyProgrammeData]]
    ) -> None:
        self._study_programmes_repository = study_programmes_repository
        self._questions_tree_generator = questions_tree_generator
        self._questions_tree_storage = question_tree_storage

    async def __call__(self) -> None:
        """
        Fetches study programmes, generates questions tree and saves it.

        :return: None
        """

        study_programmes = await self._study_programmes_repository.get_all()
        questions_tree = await self._questions_tree_generator.generate(study_programmes)
        await self._questions_tree_storage.save(questions_tree)

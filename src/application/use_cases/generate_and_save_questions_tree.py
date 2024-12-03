from src.application.interfaces import QuestionTreeGenerator
from src.domain.entities.question_tree import QuestionsTree
from src.application.interfaces import Savable, AllStudyProgrammesRepository


class GenerateAndSaveQuestionsTreeUseCase[StudyProgrammeData]:
    def __init__(
            self,
            study_programmes_source: AllStudyProgrammesRepository[StudyProgrammeData],
            questions_tree_generator: QuestionTreeGenerator[StudyProgrammeData],
            question_tree_storage: Savable[QuestionsTree[StudyProgrammeData]]
    ) -> None:
        self._study_programmes_repository = study_programmes_source
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

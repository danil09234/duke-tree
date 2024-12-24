from src.application.interfaces import QuestionTreeGraphGenerator
from src.application.interfaces import Savable, GetAllRepository
from src.domain.entities.question_tree import QuestionTree


class LoadQuestionTreesAndGenerateGraphsUseCase[StudyProgrammeData]:
    def __init__(
            self,
            questions_tree_storage: GetAllRepository[QuestionTree[StudyProgrammeData]],
            graph_generator: QuestionTreeGraphGenerator[StudyProgrammeData],
            graph_storage: Savable[str]
    ) -> None:
        self._questions_tree_repository = questions_tree_storage
        self._graph_generator = graph_generator
        self._graph_storage = graph_storage

    async def __call__(self) -> None:
        """
        Loads question trees, generates graphs and saves them.

        :return: None
        """

        question_trees = await self._questions_tree_repository.get_all()
        graphs = [self._graph_generator.generate(question_tree) for question_tree in question_trees]
        await self._graph_storage.save_multiple(graphs)

from typing import Protocol, Iterable

from src.domain.entities.question_tree import QuestionsTree
from src.domain.enums import Language


class Savable[Object](Protocol):
    async def save(self, one_object: Object) -> None:
        """
        Saves the study programme.

        :param one_object: Study programme.
        """

    async def save_multiple(self, objects: list[Object]) -> None:
        """
        Saves the list of study programmes.

        :param objects: List of study programmes.
        """


class Fetchable[Object](Protocol):
    async def fetch_all(self) -> list[Object]:
        """
        Fetches data.

        :return: Fetched data.
        """


class Creator[Object](Protocol):
    def create(self) -> Object:
        """
        Creates an object.

        :return: Created object.
        """


class WebPageLoader(Protocol):
    async def load(self, url: str) -> str:
        """
        Fetches the content of a web page.

        :param url: URL of the web page.
        :return: Content of the web page.
        """


class Parser[RawData, ParsedData](Protocol):
    def parse_one(self, data: RawData) -> ParsedData:
        """
        Parses the data.

        :param data: Data to parse.
        :return: Parsed data.
        """

    def parse_multiple(self, data: Iterable[RawData]) -> list[ParsedData]:
        """
        Parses the data.

        :param data: Data to parse.
        :return: Parsed data.
        """
        return [self.parse_one(page) for page in data]


class StudyProgrammesRepositoryByCodes[StudyProgramme](Protocol):
    async def get_by_codes(self, programmes_codes: list[str]) -> list[StudyProgramme]:
        """
        Fetches study programmes by their codes.

        :param programmes_codes: List of study programmes codes.
        :return: List of study programmes.
        """


class GetAllRepository[Object](Protocol):
    async def get_all(self) -> list[Object]:
        """
        Fetches all objects.

        :return: List of objects.
        """


class LanguageParserFactory[Parser](Protocol):
    def create(self, language: Language) -> Parser:
        """
        Creates a parser for a specific language.

        :param language: Language.
        :return: Parser.
        """


class QuestionTreeGenerator[StudyProgrammeData](Protocol):
    async def generate(self, study_programmes: list[StudyProgrammeData]) -> QuestionsTree[StudyProgrammeData]:
        """
        Generates questions tree based on study programmes.

        :param study_programmes: List of study programmes.
        :return: Questions tree.
        """

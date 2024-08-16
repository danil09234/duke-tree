from typing import Protocol, Iterable

from src.domain.entities.study_programme import StudyProgramme


class Savable[T](Protocol):
    async def save(self, one_object: T) -> None:
        """
        Saves the study programme.

        :param one_object: Study programme.
        """
        ...

    async def save_multiple(self, objects: list[T]) -> None:
        """
        Saves the list of study programmes.

        :param objects: List of study programmes.
        """
        ...


class Fetchable[T](Protocol):
    async def fetch_all(self) -> list[T]:
        """
        Fetches data.

        :return: Fetched data.
        """
        ...


class Creator[T](Protocol):
    def create(self) -> T:
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
        ...


class Parser[D, T](Protocol):
    def parse_one(self, data: D) -> T:
        """
        Parses the data.

        :param data: Data to parse.
        :return: Parsed data.
        """
        ...

    def parse_multiple(self, data: Iterable[D]) -> list[T]:
        """
        Parses the data.

        :param data: Data to parse.
        :return: Parsed data.
        """
        return [self.parse_one(page) for page in data]


class StudyProgrammeSource(Protocol):
    async def get_by_codes(self, programmes_codes: list[str]) -> list[StudyProgramme]:
        ...

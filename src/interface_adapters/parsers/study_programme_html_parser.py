from src.domain.entities.study_programme import StudyProgramme
from src.application.interfaces import Parser
from src.domain.enums.degree import Degree
from src.domain.enums.languages import Language
from src.domain.enums.study_form import StudyForm


class StudyProgrammeHtmlParser(Parser[str, StudyProgramme]):
    def _map_to_study_form(self, study_form: str) -> StudyForm:
        """
        Maps a string to a StudyForm enum.

        :param study_form: String to map.
        :return: StudyForm enum.
        """
        raise NotImplementedError

    def _map_to_degree(self, degree: str) -> Degree:
        """
        Maps a string to a Degree enum.

        :param degree: String to map.
        :return: Degree enum.
        """
        raise NotImplementedError

    def _map_to_language(self, language: str) -> Language:
        """
        Maps a string to a Language enum.

        :param language: String to map.
        :return: Language enum.
        """
        raise NotImplementedError

    def parse_one(self, page: str) -> StudyProgramme:
        """
        Extracts information about a study programme from the content of its page, returning a StudyProgramme object.

        :param page: Content of the page.
        :return: StudyProgramme object.
        """
        raise NotImplementedError

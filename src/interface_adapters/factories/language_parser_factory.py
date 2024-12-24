from src.application.interfaces import LanguageParserFactory, Parser
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.enums import Language
from src.interface_adapters.parsers.res_tuke_study_programme_html_parser import ResTukeStudyProgrammeHtmlParser


class ResTukeLanguageParserFactory(LanguageParserFactory[Parser[str, ResTukeStudyProgrammeData]]):
    def __init__(self) -> None:
        self._parsers = {language: ResTukeStudyProgrammeHtmlParser(language) for language in Language}

    def create(self, language: Language) -> Parser[str, ResTukeStudyProgrammeData]:
        """
        Creates a language parser.

        :return: Language parser.
        """
        return self._parsers[language]

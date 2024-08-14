from src.scripts.study_programmes_parser.domain.entities.study_programme import StudyProgramme
from src.scripts.study_programmes_parser.infrastructure.interfaces import Parser


class HtmlStudyProgrammeParser(Parser[str, StudyProgramme]):
    def parse_one(self, page: str) -> StudyProgramme:
        """
        Extracts information about a study programme from its page, returning a StudyProgramme object.

        :param page: URL of the page with the study programme.
        :return: StudyProgramme object.
        """
        return StudyProgramme(
            page_url="",
            name="",
            study_field="",
            level_of_degree=0,
            study_form="",
            degree="",
            length_of_study_in_years=0,
            professionally_oriented=False,
            joint_study_program=False,
            languages_of_delivery=0,
            description=""
        )

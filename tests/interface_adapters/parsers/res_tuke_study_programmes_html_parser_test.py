import pytest
from pathlib import Path

from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.parsers.res_tuke_study_programme_html_parser import ResTukeStudyProgrammeHtmlParser
from src.domain.entities.tuke_study_programme import TukeStudyProgramme
from src.domain.enums import Language, Degree, StudyForm


class TestResTukeStudyProgrammeHtmlParserOnSkPage:
    @pytest.fixture(scope="class")
    def page_parsing_results(self, res_tuke_test_page_sk: Path) -> ResTukeStudyProgrammeData:
        with open(res_tuke_test_page_sk, encoding='utf-8') as file:
            page = file.read()
        parser = ResTukeStudyProgrammeHtmlParser(Language.SLOVAK)
        return parser.parse_one(page)

    def test_name(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.name == "aplikovaná elektrotechnika"

    def test_faculty(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.faculty == "Fakulta elektrotechniky a informatiky"

    def test_study_field(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.study_field == "elektrotechnika"

    def test_study_form(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.study_form == StudyForm.PRESENT

    def test_description(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.description.startswith(
            "Absolvent študijného programu Aplikovaná elektrotechnika"
        )

    def test_learning_objectives(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.learning_objectives.startswith(
            "Absolvent bakalárskeho študijného programu Aplikovaná elektrotechnika"
        )

    def test_main_learning_outcomes(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.main_learning_outcomes.startswith(
            "Absolvent študijného programu Aplikovaná elektrotechnika má teoretické vedomosti"
        )

    def test_level_of_degree(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.level_of_degree == 1

    def test_degree(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.degree == Degree.BACHELOR

    def test_languages_of_delivery(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.languages_of_delivery == Language.SLOVAK

    def test_length_of_study(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.length_of_study_in_years == 3

    def test_professionally_oriented(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.professionally_oriented is False

    def test_joint_study_program(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.joint_study_program is False


class TestResTukeStudyProgrammeHtmlParserOnEnPage:
    @pytest.fixture(scope="class")
    def page_parsing_results(self, res_tuke_test_page_en: Path) -> ResTukeStudyProgrammeData:
        with open(res_tuke_test_page_en, encoding='utf-8') as file:
            page = file.read()
        parser = ResTukeStudyProgrammeHtmlParser(Language.ENGLISH)
        return parser.parse_one(page)

    def test_name(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.name == "aplikovaná elektrotechnika"

    def test_faculty(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.faculty == "Faculty of Electrical Engineering and Informatics"

    def test_study_field(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.study_field == "Electrical and Electronics Engineering"

    def test_study_form(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.study_form == StudyForm.PRESENT

    def test_description(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.description.startswith(
            "A graduate of the Applied Electrical Engineering study program has knowledge"
        )

    def test_learning_objectives(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.learning_objectives.startswith(
            "A graduate of the Bachelor's study program Applied Electrical Engineering will"
        )

    def test_main_learning_outcomes(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.main_learning_outcomes.startswith(
            "A graduate of the Applied Electrical Engineering study program has theoretical"
        )

    def test_level_of_degree(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.level_of_degree == 1

    def test_degree(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.degree == Degree.BACHELOR

    def test_languages_of_delivery(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.languages_of_delivery == Language.SLOVAK

    def test_length_of_study(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.length_of_study_in_years == 3

    def test_professionally_oriented(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.professionally_oriented is False

    def test_joint_study_program(self, page_parsing_results: TukeStudyProgramme) -> None:
        assert page_parsing_results.joint_study_program is False

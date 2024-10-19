from src.domain.entities.tuke_study_programme import TukeStudyProgramme
from src.application.interfaces import Parser
from src.domain.enums.degree import Degree
from src.domain.enums.languages import Language
from src.domain.enums.study_form import StudyForm
from bs4 import BeautifulSoup, Tag


class StudyProgrammeHtmlParser(Parser[str, TukeStudyProgramme]):
    _PROGRAMME_PAGE_URL_TEMPLATE = "https://www.portalvs.sk/{lang}/morho/zobrazit/{code}"

    def parse_one(self, page: str) -> TukeStudyProgramme:
        """
        Extracts information about a study programme from the content of its page, returning a StudyProgramme object.

        :param page: Content of the page.
        :return: StudyProgramme object.
        """
        soup = BeautifulSoup(page, 'html.parser')
        data = self._extract_data_from_page(soup)
        return self._create_study_programme(data)

    def _extract_data_from_page(self, soup: BeautifulSoup) -> dict[str, str]:
        """
        Extracts data from the HTML page content.

        :param soup: Parsed HTML content.
        :return: Dictionary containing study programme data.
        """
        data = {}
        data.update(self._extract_data_from_section(soup, 'div', 'col-md-8 main'))
        data.update(self._extract_data_from_section(soup, 'div', 'col-md-4 aside'))
        return data

    def _extract_data_from_section(self, soup: BeautifulSoup, tag: str, class_name: str) -> dict[str, str]:
        """
        Extracts table data from a specific section (tag and class).

        :param soup: Parsed HTML content.
        :param tag: Tag name where the table is located.
        :param class_name: Class name where the table is located.
        :return: Dictionary with extracted key-value pairs.
        """
        section = soup.find(tag, class_=class_name)
        if not section:
            return {}

        table = section.find('table', class_='table')
        if not table:
            return {}

        return self._extract_table_data(table)

    @staticmethod
    def _extract_table_data(table: Tag) -> dict[str, str]:
        """
        Extracts data from an HTML table.

        :param table: BeautifulSoup object representing the HTML table.
        :return: Dictionary with extracted key-value pairs.
        """
        data = {}
        for row in table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')

            if th and td:
                key = th.text.strip()
                value = td.text.strip()
                if key not in data:
                    data[key] = value
        return data

    def _create_study_programme(self, data: dict[str, str]) -> TukeStudyProgramme:
        """
            Creates a TukeStudyProgramme object from the extracted data.

            :param data: Dictionary containing study programme data.
            :return: TukeStudyProgramme object.
        """
        return TukeStudyProgramme(
            page_url=self._get_page_url(data),
            page_language=self._map_to_language(data.get("Jazyky poskytovania:", "") or
                                                data.get("Languages of provision:", "")),
            name=data.get("Študijný program:", "") or data.get("Study program:", ""),
            programme_code=int(data.get("Kód:", "") or data.get("Code:", "")),
            study_field=data.get("Študijný odbor:", "") or data.get("Field of study:", ""),
            level_of_degree=int((data.get("Stupeň štúdia:", "") or data.get("Level of study:", "")).replace(".", "")),
            study_form=self._map_to_study_form(data.get("Forma štúdia:", "") or data.get("Form of study:", "")),
            degree=self._map_to_degree(data.get("Stupeň štúdia:", "") or data.get("Level of study:", "")),
            length_of_study_in_years=int(data.get("Dĺžka štúdia:", "") or data.get("Length of study:", "")),
            professionally_oriented=self._map_to_professionally_oriented(data.get("Profesijne orientovaný:", "")
                                                                         or data.get("Professionally oriented:", "")),
            joint_study_program=self._map_to_joint_study_program(data.get("Spoločný študijný program:", "")
                                                                 or data.get("Common study program:", "")),
            languages_of_delivery=self._map_to_language(data.get("Jazyky poskytovania:", "") or
                                                        data.get("Languages of provision:", "")),
            description="",
            learning_objectives="",
            main_learning_outcomes="",
            faculty=data.get("Fakulta:", "") or data.get("Faculty:", "")
        )

    @classmethod
    def _get_page_url(cls, data: dict[str, str]) -> str:
        study_programme_code = data.get("Kód:", "") or data.get("Code:", "")
        language = "en" if "Code:" in data else "sk"
        return cls._PROGRAMME_PAGE_URL_TEMPLATE.format(code=study_programme_code, lang=language)

    @staticmethod
    def _map_to_language(language: str) -> Language:
        """
        Maps a string to a Language enum.

        :param language: String to map.
        :return: Language enum.
        """
        if language.lower() == 'anglický jazyk' or language.lower() == 'anglicky jazyk':
            return Language.ENGLISH
        elif language.lower() == 'slovenský jazyk' or language.lower() == 'slovensky jazyk':
            return Language.SLOVAK
        else:
            raise ValueError(f"Unknown language: {language}")

    @staticmethod
    def _map_to_study_form(study_form: str) -> StudyForm:
        """
        Maps a string to a StudyForm enum.

        :param study_form: String to map.
        :return: StudyForm enum.
        """
        if study_form.lower() == 'denná' or study_form.lower() == 'denna':
            return StudyForm.PRESENT
        elif study_form.lower() == 'externa' or study_form.lower() == 'externá':
            return StudyForm.EXTERNAL
        else:
            raise ValueError(f"Unknown study form: {study_form}")

    @staticmethod
    def _map_to_degree(degree: str) -> Degree:
        """
        Maps a string to a Degree enum.

        :param degree: String to map.
        :return: Degree enum.
        """
        if degree.lower() == '1.' or degree.lower() == '1':
            return Degree.BACHELOR
        elif degree.lower() == '2.' or degree.lower() == '2':
            return Degree.MASTER
        elif degree.lower() == '3.' or degree.lower() == '3':
            return Degree.DOCTOR
        else:
            raise ValueError(f"Unknown degree: {degree}")

    @staticmethod
    def _map_to_professionally_oriented(oriented: str) -> bool:
        """
        Maps a string to a Professionally oriented bool value

        :param oriented: String to map.
        :return: bool value ("True" or "False").
        """
        if oriented.lower() == 'áno' or oriented.lower() == 'yes':
            return True
        elif oriented.lower() == 'nie' or oriented.lower() == 'no':
            return False
        else:
            raise ValueError(f"Unknown professionally oriented value: {oriented}")

    @staticmethod
    def _map_to_joint_study_program(joint_program: str) -> bool:
        """
        Maps a string to a Joint study program bool value

        :param joint_program: String to map.
        :return: bool value ("True" or "False").
        """
        if joint_program.lower() == 'áno' or joint_program.lower() == 'yes':
            return True
        elif joint_program.lower() == 'nie' or joint_program.lower() == 'no':
            return False
        else:
            raise ValueError(f"Unknown Joint study program value: {joint_program}")

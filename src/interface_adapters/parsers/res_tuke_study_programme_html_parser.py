from typing import Dict, Any, cast
from lxml import etree
from lxml.etree import _Element

from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.application.interfaces import Parser
from src.domain.enums import Language, Degree, StudyForm
from src.interface_adapters.exceptions import ParserError


class ResTukeStudyProgrammeHtmlParser(Parser[str, ResTukeStudyProgrammeData]):
    def __init__(self, page_language: Language):
        self.page_language = page_language
        self._init_mappings()

    def _init_mappings(self) -> None:
        self._XPATH_MAPPING = {
            "title": "/html/body/main/h3/strong",
            "faculty": "/html/body/main/a[2]/span",
            "study_form": "/html/body/main/span[8]",
            "degree": "/html/body/main/span[10]",
            "length_of_study_in_years": "/html/body/main/span[12]",
            "level_of_degree": "/html/body/main/span[6]",
            "description": "/html/body/main/span[19]",
            "learning_objectives": "/html/body/main/span[20]",
            "main_learning_outcomes": "/html/body/main/span[21]",
            "professionally_oriented": "/html/body/main/span[14]",
            "study_field": "/html/body/main/span[4]",
            "joint_study_program": "/html/body/main/span[16]",
            "languages_of_delivery": "/html/body/main/span[18]",
        }
        self._DEGREE_MAPPING = {
            'Bc.': Degree.BACHELOR,
            'Ing.': Degree.MASTER,
            'PhD.': Degree.DOCTOR,
            'mgr. art.': Degree.ART_MASTER,
            'artd.': Degree.ARTD,
        }
        if self.page_language == Language.SLOVAK:
            self._STUDY_FORM_MAPPING = {
                'denná': StudyForm.PRESENT,
                'externá': StudyForm.EXTERNAL,
            }
            self._LANGUAGE_MAPPING = {
                'slovenský jazyk': Language.SLOVAK,
                'anglický jazyk': Language.ENGLISH,
            }
            self._BOOLEAN_VALUES = {'áno': True, 'nie': False}
        elif self.page_language == Language.ENGLISH:
            self._STUDY_FORM_MAPPING = {
                'present': StudyForm.PRESENT,
                'external': StudyForm.EXTERNAL,
            }
            self._LANGUAGE_MAPPING = {
                'english language': Language.ENGLISH,
                'slovak language': Language.SLOVAK,
            }
            self._BOOLEAN_VALUES = {'yes': True, 'no': False}
        else:
            raise ValueError(f"Unsupported language: {self.page_language}")

    def parse_one(self, page: str) -> ResTukeStudyProgrammeData:
        tree = etree.HTML(page)
        try:
            data = self._extract_study_programme(tree)
        except (ValueError, KeyError) as e:
            raise ParserError(f"Error parsing study programme: {e}")
        return data

    def _extract_study_programme(self, tree: _Element) -> ResTukeStudyProgrammeData:
        name = self._extract_text(tree, "title")
        study_field = self._extract_text(tree, "study_field")
        description = self._extract_text(tree, "description")
        learning_objectives = self._extract_text(tree, "learning_objectives")
        main_learning_outcomes = self._extract_text(tree, "main_learning_outcomes")
        level_of_degree = int(self._extract_text(tree, "level_of_degree"))
        study_form = self._extract_mapped_value(tree, "study_form", self._STUDY_FORM_MAPPING)
        degree = self._extract_mapped_value(tree, "degree", self._DEGREE_MAPPING)
        length_of_study_in_years = self._extract_int(tree, "length_of_study_in_years")
        professionally_oriented = self._extract_bool(tree, "professionally_oriented")
        joint_study_program = self._extract_bool(tree, "joint_study_program")
        languages_of_delivery = self._extract_mapped_value(tree, "languages_of_delivery", self._LANGUAGE_MAPPING)
        faculty = self._extract_text(tree, "faculty")

        return ResTukeStudyProgrammeData(
            name=name,
            study_field=study_field,
            level_of_degree=level_of_degree,
            study_form=study_form,
            degree=degree,
            length_of_study_in_years=length_of_study_in_years,
            professionally_oriented=professionally_oriented,
            joint_study_program=joint_study_program,
            languages_of_delivery=languages_of_delivery,
            description=description,
            learning_objectives=learning_objectives,
            main_learning_outcomes=main_learning_outcomes,
            faculty=faculty,
        )

    def _extract_text(self, tree: _Element, key: str) -> str:
        xpath = self._XPATH_MAPPING.get(key)
        if not xpath:
            raise KeyError(f"XPath not defined for key: {key}")
        elements: list[_Element] = cast(list[_Element], tree.xpath(xpath))
        if elements and elements[0].text:
            return elements[0].text.strip()
        raise ValueError(f"Missing or empty required field: {key}")

    def _extract_mapped_value(self, tree: _Element, key: str, mapping: Dict[str, Any]) -> Any:
        text = self._extract_text(tree, key).lower()
        for map_key, value in mapping.items():
            if map_key.lower() in text:
                return value
        raise ValueError(f"Invalid value for field '{key}': {text}")

    def _extract_bool(self, tree: _Element, key: str) -> bool:
        text = self._extract_text(tree, key).lower()
        return self._BOOLEAN_VALUES.get(text, False)

    def _extract_int(self, tree: _Element, key: str) -> int:
        text = self._extract_text(tree, key)
        return int(text)

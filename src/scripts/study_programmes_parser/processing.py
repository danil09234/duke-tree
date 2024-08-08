from .exceptions import InvalidUrlError
from .types import StudyProgramme

type url = str


def is_valid_url(value: str) -> bool:
    """
    Checks if the given value is a valid URL.

    :param value: URL to check.
    :return: True if the URL is valid, False otherwise.
    """
    pass


def extract_study_programme_from_its_page(page: url) -> StudyProgramme:
    """
    Extracts information about a study programme from its page, returning a StudyProgramme object.

    :param page: URL of the page with the study programme.
    :return: StudyProgramme object.
    """
    if not is_valid_url(page):
        raise InvalidUrlError("Invalid URL")

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


def parse_page_with_study_programmes(page: url) -> list[url]:
    """
    Parses a page with a list of study programmes, returning a list of URLs to the pages with the study programmes.

    :param page: URL of the page with the list of study programmes.
    :return: List of URLs to the pages with the study programmes.
    """
    if not is_valid_url(page):
        raise InvalidUrlError("Invalid URL")
    return []


def get_list_of_study_programmes_by_field_of_study(page: url) -> list[url]:
    """
    Returns a list of URLs to the pages with the study programmes extracted from the "Select by field of study" section.

    :param page: URL of the page with the sorting options
    :return: List of URLs to the pages with the study programmes.
    """
    if not is_valid_url(page):
        raise InvalidUrlError("Invalid URL")
    return []


def get_list_of_study_programmes_by_faculty(page: url) -> list[url]:
    """
    Returns a list of URLs to the pages with the study programmes extracted from the "Select by faculty" section.

    :param page: URL of the page with the sorting options
    :return: List of URLs to the pages with the study programmes.
    """
    if not is_valid_url(page):
        raise InvalidUrlError("Invalid URL")
    return []

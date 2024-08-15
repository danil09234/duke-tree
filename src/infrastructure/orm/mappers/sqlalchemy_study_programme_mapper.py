from src.domain.enums import StudyForm, Degree, Language
from src.infrastructure.orm.enums import StudyForm as StudyFormORM, Degree as DegreeORM, Language as LanguageORM
from src.infrastructure.interfaces import EntityMapper
from src.infrastructure.orm.models import StudyProgramme as StudyProgrammeORM
from src.domain.entities.study_programme import StudyProgramme


class SQLAlchemyStudyProgrammeMapper(EntityMapper[StudyProgramme, StudyProgrammeORM]):
    @staticmethod
    def _study_form_to_orm_mapper(study_form: StudyForm) -> StudyFormORM:
        return StudyFormORM(study_form.value)

    @staticmethod
    def _degree_to_orm_mapper(degree: Degree) -> DegreeORM:
        return DegreeORM(degree.value)

    @staticmethod
    def _language_to_orm_mapper(language: Language) -> LanguageORM:
        return LanguageORM(language.value)

    @staticmethod
    def _study_form_to_entity_mapper(study_form: StudyFormORM) -> StudyForm:
        return StudyForm(study_form.value)

    @staticmethod
    def _degree_to_entity_mapper(degree: DegreeORM) -> Degree:
        return Degree(degree.value)

    @staticmethod
    def _language_to_entity_mapper(language: LanguageORM) -> Language:
        return Language(language.value)

    async def to_entity(self, source: StudyProgrammeORM) -> StudyProgramme:
        return StudyProgramme(
            page_url=source.page_url,
            name=source.name,
            study_field=source.study_field,
            level_of_degree=source.level_of_degree,
            study_form=self._study_form_to_entity_mapper(source.study_form),
            degree=self._degree_to_entity_mapper(source.degree),
            length_of_study_in_years=source.length_of_study_in_years,
            professionally_oriented=source.professionally_oriented,
            joint_study_program=source.joint_study_program,
            languages_of_delivery=self._language_to_entity_mapper(source.languages_of_delivery),
            description=source.description,
        )

    async def from_entity(self, entity: StudyProgramme) -> StudyProgrammeORM:
        return StudyProgrammeORM(
            page_url=entity.page_url,
            name=entity.name,
            study_field=entity.study_field,
            level_of_degree=entity.level_of_degree,
            study_form=self._study_form_to_orm_mapper(entity.study_form),
            degree=self._degree_to_orm_mapper(entity.degree),
            length_of_study_in_years=entity.length_of_study_in_years,
            professionally_oriented=entity.professionally_oriented,
            joint_study_program=entity.joint_study_program,
            languages_of_delivery=self._language_to_orm_mapper(entity.languages_of_delivery),
            description=entity.description,
        )

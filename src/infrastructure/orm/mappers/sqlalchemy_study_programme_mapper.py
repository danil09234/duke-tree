from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page, PageMetadata
from src.domain.enums import StudyForm, Degree, Language
from src.infrastructure.orm.enums import StudyForm as StudyFormORM, Degree as DegreeORM, Language as LanguageORM
from src.infrastructure.interfaces import EntityMapper
from src.infrastructure.orm.models import StudyProgramme as StudyProgrammeORM


class SQLAlchemyStudyProgrammeMapper(
    EntityMapper[Page[ResTukeStudyProgrammeData], StudyProgrammeORM]
):
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

    async def to_entity(self, source: StudyProgrammeORM) -> Page[ResTukeStudyProgrammeData]:
        data = ResTukeStudyProgrammeData(
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
            learning_objectives=source.learning_objectives,
            main_learning_outcomes=source.main_learning_outcomes,
            faculty=source.faculty,
        )
        metadata = PageMetadata(
            language=self._language_to_entity_mapper(source.page_language),
            code=source.programme_code,
            url=source.page_url
        )
        return Page(data=data, metadata=metadata)

    async def from_entity(self, entity: Page[ResTukeStudyProgrammeData]) -> StudyProgrammeORM:
        return StudyProgrammeORM(
            page_url=entity.metadata.url,
            programme_code=entity.metadata.code,
            page_language=self._language_to_orm_mapper(entity.metadata.language),
            name=entity.data.name,
            study_field=entity.data.study_field,
            level_of_degree=entity.data.level_of_degree,
            study_form=self._study_form_to_orm_mapper(entity.data.study_form),
            degree=self._degree_to_orm_mapper(entity.data.degree),
            length_of_study_in_years=entity.data.length_of_study_in_years,
            professionally_oriented=entity.data.professionally_oriented,
            joint_study_program=entity.data.joint_study_program,
            languages_of_delivery=self._language_to_orm_mapper(
                entity.data.languages_of_delivery
            ),
            description=entity.data.description,
            learning_objectives=entity.data.learning_objectives,
            main_learning_outcomes=entity.data.main_learning_outcomes,
            faculty=entity.data.faculty,
        )

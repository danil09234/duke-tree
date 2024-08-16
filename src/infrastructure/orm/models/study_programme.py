from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.orm.models import Base
from src.infrastructure.orm.enums import StudyForm, Degree, Language
from sqlalchemy import Enum as SQLAlchemyEnum


class StudyProgramme(Base):
    __tablename__ = 'study_programmes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    page_url: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    study_field: Mapped[str] = mapped_column(String, nullable=False)
    level_of_degree: Mapped[int] = mapped_column(Integer, nullable=False)
    study_form: Mapped[StudyForm] = mapped_column(SQLAlchemyEnum(StudyForm), nullable=False)
    degree: Mapped[Degree] = mapped_column(SQLAlchemyEnum(Degree), nullable=False)
    length_of_study_in_years: Mapped[int] = mapped_column(Integer, nullable=False)
    professionally_oriented: Mapped[bool] = mapped_column(Integer, nullable=False)
    joint_study_program: Mapped[bool] = mapped_column(Integer, nullable=False)
    languages_of_delivery: Mapped[Language] = mapped_column(SQLAlchemyEnum(Language), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    learning_objectives: Mapped[str] = mapped_column(Text, nullable=False)
    main_learning_outcomes: Mapped[str] = mapped_column(Text, nullable=False)

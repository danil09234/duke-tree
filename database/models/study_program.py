from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import StudyForm, Degree


class StudyProgram(Base):
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
    languages_of_delivery: Mapped[int] = mapped_column(Integer, ForeignKey("languages.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

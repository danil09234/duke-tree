from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page

QuestionNode = OptionsQuestion[Page[ResTukeStudyProgrammeData]] | BinaryQuestion[Page[ResTukeStudyProgrammeData]]
AnswerNode = Page[ResTukeStudyProgrammeData]
TreeNode = QuestionNode | AnswerNode

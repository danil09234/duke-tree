from src.interface_adapters.gateways.study_programmes_gateway_base import StudyProgrammesGatewayBase
from src.domain.entities import TukeStudyProgramme
from src.application.interfaces import StudyProgrammesSource


class TukeStudyProgrammesGateway(
    StudyProgrammesGatewayBase[TukeStudyProgramme],
    StudyProgrammesSource[TukeStudyProgramme]
):
    _URL_TEMPLATE = "https://res.tuke.sk/api/programme_detail/{code}?lang={lang}"

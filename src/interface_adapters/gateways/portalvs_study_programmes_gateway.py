from src.interface_adapters.gateways.study_programmes_gateway_base import StudyProgrammesGatewayBase
from src.domain.entities import TukeStudyProgramme
from src.application.interfaces import StudyProgrammesSource


class PortalvsStudyProgrammesGateway(
    StudyProgrammesGatewayBase[TukeStudyProgramme],
    StudyProgrammesSource[TukeStudyProgramme]
):
    _URL_TEMPLATE = "https://www.portalvs.sk/{lang}/morho/zobrazit/{code}"

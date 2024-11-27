from src.interface_adapters.gateways.study_programmes_gateway_base import StudyProgrammesGatewayBase, Page
from src.application.interfaces import StudyProgrammesSource


class PortalvsStudyProgrammesGateway[Data](
    StudyProgrammesGatewayBase[Data],
    StudyProgrammesSource[Page[Data]]
):
    _URL_TEMPLATE = "https://www.portalvs.sk/{lang}/morho/zobrazit/{code}"

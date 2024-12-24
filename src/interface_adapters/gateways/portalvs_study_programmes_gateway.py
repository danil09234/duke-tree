from src.application.interfaces import StudyProgrammesRepositoryByCodes
from src.interface_adapters.gateways.study_programmes_gateway_base import StudyProgrammesGatewayBase, Page


class PortalvsStudyProgrammesGateway[Data](
    StudyProgrammesGatewayBase[Data],
    StudyProgrammesRepositoryByCodes[Page[Data]]
):
    _URL_TEMPLATE = "https://www.portalvs.sk/{lang}/morho/zobrazit/{code}"

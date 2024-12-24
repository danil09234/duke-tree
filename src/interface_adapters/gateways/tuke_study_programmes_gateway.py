from src.interface_adapters.gateways.study_programmes_gateway_base import StudyProgrammesGatewayBase, Page
from src.application.interfaces import StudyProgrammesRepositoryByCodes


class ResTukeStudyProgrammesGateway[PageContent](
    StudyProgrammesGatewayBase[PageContent],
    StudyProgrammesRepositoryByCodes[Page[PageContent]]
):
    _URL_TEMPLATE = "https://res.tuke.sk/api/programme_detail/{code}?lang={lang}"


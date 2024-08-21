from domain.commands.environment_commands import GetParameter
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.ports.environment_service import EnvironmentService


def get_parameter(
    command: GetParameter, environment_service: EnvironmentService
) -> str:
    value = environment_service.get_parameter(
        GetParameter.name, is_encrypted=GetParameter.is_encrypted
    )
    if not value:
        raise InvalidEnvironmentSetup(GetParameter.name)
    return value

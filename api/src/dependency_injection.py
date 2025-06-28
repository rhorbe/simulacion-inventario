from api.src.domain.repository.config import Config
from api.src.infra.repository.yml_config_repository import YmlConfigRepository
from api.src.application.command_bus import CommandBus
from api.src.application.handlers.simular_command_handler import SimularCommandHandler
from api.src.application.commands.simular_command import SimularCommand


def get_config() -> Config:
    """Función de dependencia que proporciona la implementación de Config."""
    return YmlConfigRepository()


def get_command_bus() -> CommandBus:
    """Proporciona una instancia del bus de comandos configurado"""
    bus = CommandBus()
    bus.register_handler(SimularCommand, SimularCommandHandler())
    return bus 
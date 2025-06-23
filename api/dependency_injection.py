from api.domain.repository.config import Config
from api.infra.repository.yml_config_repository import YmlConfigRepository


def get_config() -> Config:
    """Función de dependencia que proporciona la implementación de Config."""
    return YmlConfigRepository() 
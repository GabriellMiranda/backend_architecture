import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Aplication"
    description: str = "API REST privada para obter dados de cotas precificados."
    version: str = "0.1.0"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    root_path: str = f'/{os.environ["API_ROOT_PATH"]}'

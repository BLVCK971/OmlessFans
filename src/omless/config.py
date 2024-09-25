import logging
import os
from urllib import parse
from typing import List, Any
from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

from omless.constants import Environment


log = logging.getLogger(__name__)

RUN_MODE = os.environ.get('RUN_MODE', 'NONE')

PROJECT_NAME = "NET-ENT-ATMP"

DATA_PATH = "C:\\DATA\\"
CONFIG_PATH = "C:\\ENV\\"
ENV_FILE = "\\.env"

if RUN_MODE == "PROD":
    DATA_PATH = "/home/ssm-user/DATA/"
    CONFIG_PATH = "/home/ssm-user/ENV/"
    ENV_FILE = "/.env"
    

config = Config(CONFIG_PATH + PROJECT_NAME + ENV_FILE)




# class CustomBaseSettings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=".env", env_file_encoding="utf-8", extra="ignore"
#     )


# class APIConfig(CustomBaseSettings):

#     ENVIRONMENT: Environment = Environment.PRODUCTION

#     CORS_ORIGINS: list[str] = ["*"]
#     CORS_ORIGINS_REGEX: str | None = None
#     CORS_HEADERS: list[str] = ["*"]

#     APP_VERSION: str = "0.1"


# settings = APIConfig()


# class BaseConfigurationModel(BaseModel):
#     """Base configuration model used by all config options."""

#     pass


# def get_env_tags(tag_list: List[str]) -> dict:
#     """Create dictionary of available env tags."""
#     tags = {}
#     for t in tag_list:
#         tag_key, env_key = t.split(":")

#         env_value = os.environ.get(env_key)

#         if env_value:
#             tags.update({tag_key: env_value})

#     return tags


LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

# ENV_TAG_LIST = config("ENV_TAGS", cast=CommaSeparatedStrings, default="")
# ENV_TAGS = get_env_tags(ENV_TAG_LIST)


# API Conf
app_configs: dict[str, Any] = {
    "title": "Omless API",
    "description": "Welcome to Omless's API documentation! Here you will able to discover all of the ways you can interact with the Omless API.",
    "root_path": "/api/v1",
   "docs_url": "/swagger",
    "openapi_url": "/docs/openapi.json",
    "redoc_url": "/redoc",
}

# Cache la doc Swagger hors dev
# if not settings.ENVIRONMENT.is_debug:
#     app_configs["openapi_url"] = None  # hide docs

# ajouter la version en Prod
# if settings.ENVIRONMENT.is_deployed:
#     app_configs["root_path"] = f"/v{settings.APP_VERSION}"

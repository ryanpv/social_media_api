from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    LOGTAIL_API_KEY: Optional[str] = None
    MAILGUN_DOMAIN: Optional[str] = None
    MAILGUN_API_KEY: Optional[str] = None
    PWD_SECRET_KEY: Optional[str] = None
    B2_KEY_ID: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = None
    DEEPAI_API_KEY: Optional[str] = None


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_", extra="ignore")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_", extra="ignore")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///./test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_", extra="ignore")


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)

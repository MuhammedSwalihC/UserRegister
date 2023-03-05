"""Config settings for for development, testing and production environments."""
from __future__ import annotations

import os
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

DB_DEV = "sqlite:///" + str(BASE_PATH / "register_db_dev.db")
DB_TEST = "sqlite:///" + str(BASE_PATH / "register_db_test.db")
DB_PROD = "sqlite:///" + str(BASE_PATH / "register_db_prod.db")


class Config:
    """Base configuration."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = DB_TEST


class DevelopmentConfig(Config):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", DB_DEV)
    SECRET_KEY = os.getenv("SECRET_KEY", "JGHJGA$)DGDG%$&*2D767676^67")
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", DB_PROD)
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "JGHhgsrJNADDGA$)DGDG%$&*2DSRgfserSDK67676^67",
    )
    DEBUG = False


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)

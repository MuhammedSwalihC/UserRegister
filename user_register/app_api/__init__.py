""" Application initializer """

from __future__ import annotations
from importlib import import_module
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
import warnings

warnings.filterwarnings("ignore")

from .config import get_config

db = SQLAlchemy()
migrate = Migrate()

config_file = import_module("app_api.config")
configuration = getattr(config_file, "get_config")
cors = CORS()


def create_app(config_name):
    """Initialize flask application

    Returns:
        return app object with wsgi proxy
    """
    app = Flask("hire-bot-client")
    app.url_map.strict_slashes = False
    app.config.from_object(get_config(config_name))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
    cors.init_app(app)
    db.init_app(app)
    JWTManager(app)
    migrate.init_app(app, db)
    return app

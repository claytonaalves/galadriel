""" Aplicacao principal
"""
from flask import Flask, Blueprint
from .database import db
from .chamados.controllers import chamados_blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(chamados_blueprint, url_prefix="/chamados")

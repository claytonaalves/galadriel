""" Aplicacao principal
"""
from flask import Flask, Blueprint
from .database import db
from .chamados.controllers import chamados_blueprint
from .excecoes.controllers import excecoes_blueprint
from .formatters import register_formatters

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_formatters(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(chamados_blueprint, url_prefix="/chamados")
    app.register_blueprint(excecoes_blueprint, url_prefix="/excecoes")

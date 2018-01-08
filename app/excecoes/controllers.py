from flask import Blueprint, render_template

from ello.excecoes import todas_excecoes, obtem_excecao, db

excecoes_blueprint = Blueprint('excecoes', __name__)


@excecoes_blueprint.route('/')
def index_excecoes():
    return render_template('excecoes/index.html', excecoes=todas_excecoes(db))


@excecoes_blueprint.route('/<_id>')
def detalhe_excecao(_id):
    excecao = obtem_excecao(_id, db)
    return render_template('excecoes/excecao.html', excecao=excecao)


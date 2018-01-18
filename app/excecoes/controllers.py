from flask import Blueprint, render_template, request

from ..pagination import Paginate

from ello.excecoes import (
    db,
    todas_excecoes, 
    todas_excecoes_por_cliente,
    obtem_excecao
 )


excecoes_blueprint = Blueprint('excecoes', __name__)

@excecoes_blueprint.route('/')
def index():
    page_number = int(request.args.get('p', '0'), 10)
    pages = Paginate(db.exceptions.find().count(), page_number)
    matricula = request.args.get('matricula')

    if matricula:
        excecoes = todas_excecoes_por_cliente(db, matricula)
    else:
        excecoes = todas_excecoes(db, pages.limit, pages.offset)
    return render_template('excecoes/index.html', excecoes=excecoes, pages=pages)


@excecoes_blueprint.route('/<_id>')
def detalhe_excecao(_id):
    excecao = obtem_excecao(_id, db)
    return render_template('excecoes/excecao.html', excecao=excecao)


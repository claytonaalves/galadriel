from flask import Blueprint, render_template, request

from ..pagination import Pager

from ello.excecoes import (
    db,
    todas_excecoes, 
    todas_excecoes_por_cliente,
    obtem_excecao
 )


excecoes_blueprint = Blueprint('excecoes', __name__)

@excecoes_blueprint.route('/')
def index():
    page = int(request.args.get('p', '1'), 10)
    count = db.exceptions.find().count()
    data = range(count)
    pager = Pager(page, count)
    pages = pager.get_pages()
    skip = (page - 1) * 10
    limit = 10
    #data_to_show = data[skip: skip + limit]
    excecoes = todas_excecoes(db, limit, skip)
    return render_template('excecoes/index.html', pages=pages, excecoes=excecoes)

@excecoes_blueprint.route('/<_id>')
def detalhe_excecao(_id):
    excecao = obtem_excecao(_id, db)
    return render_template('excecoes/excecao.html', excecao=excecao)


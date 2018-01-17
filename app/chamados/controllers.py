from flask import Blueprint, render_template

from .models import Chamado, ultimos_chamados_em_aberto

chamados_blueprint = Blueprint('chamados', __name__)


@chamados_blueprint.route('/')
def index():
    chamados = ultimos_chamados_em_aberto()
    return render_template('chamados/index.html', chamados=chamados)


@chamados_blueprint.route('/<_id>')
def detalhe_chamado(_id):
    chamado = Chamado.query.filter_by(id_chamado=_id).one()
    comentarios = chamado.obtem_comentarios().all()
    return render_template('chamados/detalhe.html', chamado=chamado, comentarios=comentarios)
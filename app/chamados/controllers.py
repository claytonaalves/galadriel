from flask import Blueprint, render_template

from .models import Chamado, ultimos_chamados_em_aberto

chamados_blueprint = Blueprint('chamados', __name__)


@chamados_blueprint.route('/')
def index_chamados():
    chamados = ultimos_chamados_em_aberto()
    return render_template('chamados/index.html', chamados=chamados)
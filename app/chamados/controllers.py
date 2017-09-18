from flask import Blueprint, render_template

from .models import Chamado

chamados_blueprint = Blueprint('chamados', __name__)


@chamados_blueprint.route('/')
def index_chamados():
    chamados = Chamado.query.all()
    return render_template('chamados/index.html', chamados=chamados)

import json

from flask import Blueprint, render_template

# from .models import Chamado, ultimos_chamados_em_aberto

from ..database import db

graficos_blueprint = Blueprint('graficos', __name__)


@graficos_blueprint.route('/')
def index():
    res = db.engine.execute("""
SELECT COUNT(*), a.TIPOEMPRESA
FROM TRECCLIENTE a
where 
    ativo='S' 
    and a.TIPOEMPRESA<>'INDEFINIDO'
    and a.TIPOEMPRESA<>'SOFTWAREHOUSE'
    and a.tipoempresa is not null
GROUP BY a.TIPOEMPRESA
order by 1
    """).fetchall()

    dataset1 = []
    dataset1.append(['Tipo', 'Quantidade'])
    for quantidade, tipo in res:
        if quantidade>4:
            dataset1.append([tipo, quantidade])

    dataset2 = []
    dataset2.append(['Tipo', 'Quantidade'])
    for quantidade, tipo in res:
        if quantidade<5:
            dataset2.append([tipo, quantidade])

    dataset1 = json.dumps(dataset1)
    dataset2 = json.dumps(dataset2)


    return render_template('graficos/index.html', dataset1=dataset1, dataset2=dataset2)

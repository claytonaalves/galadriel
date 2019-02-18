# encoding: utf8
from __future__ import division

import json
from collections import Counter

from flask import Blueprint, render_template, jsonify

from ..database import db
from ..cache import cache

graficos_blueprint = Blueprint('graficos', __name__)


@graficos_blueprint.route('/')
def index():
    return render_template('graficos/index.html')


@graficos_blueprint.route('/clientes')
def graficos_clientes():
    return render_template('graficos/clientes.html')


@graficos_blueprint.route('/empresas')
@cache.cached(timeout=180)
def estatisticas_empresas():
    res = db.engine.execute("""
SELECT COUNT(*), a.TIPOEMPRESA
FROM TRECCLIENTE a
where 
    ativo='S' 
    and a.TIPOEMPRESA<>'INDEFINIDO'
    and a.TIPOEMPRESA<>'SOFTWAREHOUSE'
    and a.tipoempresa is not null
GROUP BY a.TIPOEMPRESA
HAVING COUNT(*) > 4
order by 1
    """).fetchall()

    dataset = []
    for qtde, tipo_empresa in res:
        dataset.append({"name": tipo_empresa, "y": qtde})
    return jsonify(dataset)


@graficos_blueprint.route('/chamados_finalizados')
@cache.cached(timeout=180)
def estatisticas_chamados_finalizados():
    #chamados concluídos nos últimos 7 dias
    res = db.engine.execute("""
select a.responsavel, b.nome, count(*) as qtde
from TSOLSOLICITACAO a
left join TGERUSUARIO b on (a.responsavel=b.IDUSUARIO)
where 
    aberturadata>=current_date-7
    and situacao=3
group by a.responsavel, b.nome""")
    dataset = []
    for _, nome, qtde in res:
        dataset.append({"name": nome, "y": qtde})
    return jsonify(dataset)


@graficos_blueprint.route('/chamados_em_aberto')
@cache.cached(timeout=180)
def estatisticas_chamados_em_aberto():
    res = db.engine.execute("""
select a.responsavel, b.nome, count(*) as qtde
from TSOLSOLICITACAO a
left join TGERUSUARIO b on (a.responsavel=b.IDUSUARIO)
where 
    situacao=1
    and responsavel is not null
group by a.responsavel, b.nome
""")
    dataset = []
    for _, nome, qtde in res:
        dataset.append({"name": nome, "y": qtde})
    return jsonify(dataset)


@graficos_blueprint.route('/top_5_chamados_por_cliente')
@cache.cached(timeout=180)
def estatisticas_chamados_por_cliente():
    res = db.engine.execute("""
SELECT first 5 a.idcliente, b.FANTASIA, count(*)
FROM TSOLSOLICITACAO a
left join treccliente b on (b.idcliente=a.IDCLIENTE)
where a.ABERTURADATA >= current_date - 30
group by a.IDCLIENTE, b.FANTASIA
order by 3 desc
""")
    dataset = []
    for _, nome, qtde in res:
        dataset.append({"name": nome, "y": qtde})
    return jsonify(dataset)


@graficos_blueprint.route('/versao_windows')
@cache.cached(timeout=180)
def estatisticas_versao_windows():
    res = db.engine.execute("""
SELECT a.VERSAO_WINDOWS, count(*)
FROM TAUTENTICACOES a
where data >= current_date-30
group by a.VERSAO_WINDOWS
""")
    counter = Counter()
    for versao, qtde in res:
        versao = versao.split('-')[0].strip()
        counter.update({versao: qtde})
    total = sum(counter.values())
    dataset = []
    # transforma valores em percentual
    for item, value in counter.items():
        percentual = round((value * 100) / total, 2)
        dataset.append({"name": item, "y": percentual})
    return jsonify(dataset)


@graficos_blueprint.route('/resolucoes')
@cache.cached(timeout=180)
def estatisticas_resolucoes():
    res = db.engine.execute("""
SELECT a.RESOLUCAO, count(*)
FROM TAUTENTICACOES a
where data >= current_date-30
group by a.RESOLUCAO
""")
    counter = Counter()
    for resolucao, qtde in res:
        resolucao = resolucao.strip()
        counter.update({resolucao: qtde})
    total = sum(counter.values())
    dataset = []
    # transforma valores em percentual
    for item, value in counter.items():
        percentual = round((value * 100) / total, 2)
        dataset.append({"name": item, "y": percentual})
    return jsonify(dataset)


@graficos_blueprint.route('/versoes_em_uso')
@cache.cached(timeout=180)
def estatisticas_versoes_em_uso():
    res = db.engine.execute("""
SELECT a.versao, count(*)
FROM TAUTENTICACOES a
where data >= current_date-30
group by a.versao
""")
    counter = Counter()
    for versao, qtde in res:
        versao = '.'.join(versao.split('.')[:3])
        counter.update({versao: qtde})
    total = sum(counter.values())
    dataset = []
    # transforma valores em percentual
    for item, value in counter.items():
        percentual = round((value * 100) / total, 2)
        dataset.append({"name": item, "y": percentual})
    return jsonify(dataset)


@graficos_blueprint.route('/clientes_internet')
@cache.cached(timeout=86400)
def estatisticas_clientes_internet():
    res = db.engine.execute("""
with autenticacoes_ultimos_7_dias as (
    SELECT DISTINCT t.IDCLIENTE
    FROM TAUTENTICACOES t
    WHERE t.DATA >= CURRENT_DATE - 7
),
clientes_ativos as (
    select 
        cli.idcliente, cli.nome, cli.fantasia
    from treccliente cli
    where cli.ativo='S'
)
select cli.idcliente, case when aut.idcliente is null THEN 'NAO' else 'SIM' END AS POSSUI_INTERNET
from clientes_ativos cli 
left join autenticacoes_ultimos_7_dias aut on (cli.idcliente=aut.idcliente)
order by aut.idcliente
""")

    # Ignorar estes clientes
    # 469 TERRA DO BOI
    # 399 CASAS DAS ANTENAS
    # 459 NAFTA TRANSPORTES
    # 463 BMG MADEIRAS - CT-E
    # 458 TRANSPORTES FRANCA
    # 208 CONSUMIDOR / ORÇAMENTOS

    clientes_ignorados = (469, 399, 459, 463, 458, 208)
    com_internet = 0
    sem_internet = 0
    for id_cliente, possui_internet in res:
        if id_cliente in clientes_ignorados:
            continue
        if possui_internet == "SIM":
            com_internet += 1
        else:
            sem_internet += 1
    dataset = [
        {"name": "Com Internet", "y": com_internet},
        {"name": "Sem Internet", "y": sem_internet}
    ]
    return jsonify(dataset)


@graficos_blueprint.route('/clientes_por_cidade')
@cache.cached(timeout=86400)
def estatisticas_clientes_por_cidade():
    res = db.engine.execute("""\
SELECT
  cid.nome,
  COUNT(*)
FROM TRecCliente cli
LEFT JOIN TGERCIDADE cid ON (cid.IDCIDADE=cli.IDCIDADE)
WHERE cli.Ativo='S'
GROUP BY cli.IdCidade, cid.nome
HAVING COUNT(*)>1
ORDER BY 2 DESC;
""")
    dataset = []
    for cidade, qtde in res:
        dataset.append([cidade, qtde])
    return jsonify(dataset)

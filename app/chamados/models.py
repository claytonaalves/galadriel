from sqlalchemy import desc
from app.database import db


class Chamado(db.Model):
    __tablename__ = 'TSOLSOLICITACAO'
    idsolicitacao = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.String(2))
    solicitante = db.Column(db.Text)
    situacao = db.Column(db.String(255))
    descricao = db.Column(db.Text())
    solicitante = db.Column(db.String(30))
    aberturadata = db.Column(db.Date())
    aberturahora = db.Column(db.Time())
    
    def __init__(self):
        self.senha = '1234'


def ultimos_chamados_em_aberto():
    return (
        Chamado.query
            .filter_by(situacao='1')
            .order_by(desc(Chamado.idsolicitacao))
            .limit(30)
    )
# encoding: utf8

from sqlalchemy import ForeignKey, desc
from sqlalchemy.orm import relationship
from app.database import db


class Chamado(db.Model):
    __tablename__ = 'TSOLSOLICITACAO'
    id_chamado = db.Column('idsolicitacao', db.Integer, primary_key=True)
    idcliente = db.Column(db.String(2))
    solicitante = db.Column(db.Text)
    situacao = db.Column(db.String(255))
    descricao = db.Column(db.Text())
    solicitante = db.Column(db.String(30))
    data_abertura = db.Column('aberturadata', db.Date())
    aberturahora = db.Column(db.Time())
    cliente = relationship('Cliente', primaryjoin='foreign(Chamado.idcliente) == remote(Cliente.id_cliente)')
    
    def obtem_titulo(self):
        descricao = self.descricao or u'Sem descrição'
        linhas_descricao = descricao.splitlines()
        titulo = linhas_descricao[0]
        # self.descricao = ''.join(linhas_descricao[1:])
        return titulo

    def obtem_comentarios(self):
        return Comentario.query.filter_by(id_chamado=self.id_chamado)


class Comentario(db.Model):
    __tablename__ = "TSOLEVENTO"
    id_empresa = db.Column('empresa', db.Integer, primary_key=True)
    id_chamado = db.Column('idsolicitacao', db.Integer, primary_key=True)
    id_comentario = db.Column('idevento', db.Integer, ForeignKey('chamado.id_chamado'), primary_key=True)
    data = db.Column(db.Date())
    hora = db.Column(db.Time())
    id_operador = db.Column('idoperador', db.Integer)
    descricao = db.Column(db.Text)


class Cliente(db.Model):
    __tablename__ = "TRECCLIENTE"
    id_cliente = db.Column('idcliente', db.Integer, primary_key=True)
    nome = db.Column(db.String(60))


def ultimos_chamados_em_aberto():
    return (
        Chamado.query
            .filter_by(situacao='1')
            .order_by(desc(Chamado.id_chamado))
            .limit(30)
    )
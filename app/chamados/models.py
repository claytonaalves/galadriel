# encoding: utf8
from __future__ import unicode_literals

from sqlalchemy import ForeignKey, desc, or_
from sqlalchemy.orm import relationship
from app.database import db


class Responsavel(db.Model):
    __tablename__ = "TGERUSUARIO"
    id_usuario = db.Column('idusuario', db.Integer, primary_key=True)
    nome = db.Column(db.String(60))
    #chamado = relationship("Chamado", back_populates="TGERUSUARIO")


class Chamado(db.Model):
    __tablename__ = 'TSOLSOLICITACAO'
    id_chamado = db.Column('idsolicitacao', db.Integer, primary_key=True)
    idcliente = db.Column(db.String(2))
    relator = db.Column('solicitante', db.Text)
    situacao = db.Column(db.Integer)
    descricao = db.Column(db.Text())
    data_abertura = db.Column('aberturadata', db.Date())
    aberturahora = db.Column(db.Time())
    cliente = relationship('Cliente', primaryjoin='foreign(Chamado.idcliente) == remote(Cliente.id_cliente)')
    #responsavel = relationship('Responsavel', primaryjoin='foreign(Chamado.responsavel) == remote(Responsavel.id_usuario)')
    id_responsavel = db.Column('responsavel', db.Integer, ForeignKey('TGERUSUARIO.idusuario'))
    responsavel = relationship('Responsavel')
    
    def obtem_titulo(self):
        descricao = self.descricao or u'Sem descrição'
        linhas_descricao = descricao.splitlines()
        titulo = linhas_descricao[0]
        # self.descricao = ''.join(linhas_descricao[1:])

        # Normalizar o título pq tem gente que só vive com o CAPSLOCK ligado
        if titulo.isupper():
            titulo = titulo.capitalize()

        return titulo

    def obtem_comentarios(self):
        return Comentario.query.filter_by(id_chamado=self.id_chamado)

    def obtem_status(self):
        if self.situacao==1:
            return "Aguardando"
        elif self.situacao==2:
            return "Executando"
        else:
            return "Concluído"


class Comentario(db.Model):
    __tablename__ = "TSOLEVENTO"
    id_empresa = db.Column('empresa', db.Integer, primary_key=True)
    id_chamado = db.Column('idsolicitacao', db.Integer, primary_key=True)
    id_comentario = db.Column('idevento', db.Integer, ForeignKey('chamado.id_chamado'), primary_key=True)
    data = db.Column(db.Date())
    hora = db.Column(db.Time())
    id_operador = db.Column('idoperador', db.Integer)
    descricao = db.Column(db.Text)
    id_operador = db.Column('idoperador', db.Integer, ForeignKey('TGERUSUARIO.idusuario'))
    responsavel = relationship('Responsavel')


class Cliente(db.Model):
    __tablename__ = "TRECCLIENTE"
    id_cliente = db.Column('idcliente', db.Integer, primary_key=True)
    nome = db.Column(db.String(60))


def ultimos_chamados_em_aberto():
    return (
        Chamado.query
            .filter(or_(Chamado.situacao==1, Chamado.situacao==2))
            .order_by(desc(Chamado.id_chamado))
            .limit(50)
    )

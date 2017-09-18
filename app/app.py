""" Aplicacao principal
"""
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'firebird+fdb://sysdba:masterkey@/C:/Ello/Dados/ELLO.ELLO?charset=latin1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'TSOLSOLICITACAO'
    idsolicitacao = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.String(2))
    solicitante = db.Column(db.Text)
    situacao = db.Column(db.String(255))
     = db.Column(db.String(80))

    def __init__(self):
        self.senha = '11234'

@app.route('/')
def relacao_de_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/novousuario/<nome>')
def insere_novo_usuario(nome):
    usuario = Usuario()
    usuario.nome = nome
    db.session.add(usuario)
    db.session.commit()
    return redirect('/usuarios')


# db.create_all()

app.run()

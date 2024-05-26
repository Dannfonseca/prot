from app.routes import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Permissao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)

class Pessoa(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    senha_hash = db.Column(db.String(128))
    permissao_id = db.Column(db.Integer, db.ForeignKey('permissao.id'))
    endereco = db.relationship('Endereco', backref='pessoa', uselist=False)

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

@login.user_loader
def load_user(id):
    return Pessoa.query.get(int(id))

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(128))
    numero = db.Column(db.Integer)
    cep = db.Column(db.String(9))
    cidade = db.Column(db.String(64))
    estado = db.Column(db.String(2))
    complemento = db.Column(db.String(128))
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))

class Estabelecimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))

class Pagador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64))
    valor_total = db.Column(db.BigInteger)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))
    pessoa = db.relationship('Pessoa', backref='pagador')

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))
    status = db.Column(db.String(64))
    valor_total = db.Column(db.BigInteger)
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimento.id'))
    pagador_id = db.Column(db.Integer, db.ForeignKey('pagador.id'))
    estabelecimento = db.relationship('Estabelecimento', backref='pedidos')
    pagador = db.relationship('Pagador', backref='pedidos')

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))
    preco = db.Column(db.String(64))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref='produtos')

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))

class Consumo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia_consumo = db.Column(db.Date)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    pedido = db.relationship('Pedido', backref='consumos')
    produto = db.relationship('Produto', backref='consumos')

class Medida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))

class Pix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave_pix = db.Column(db.String(128))
    nome = db.Column(db.String(128))
    tipo = db.Column(db.String(64))
    pagador_id = db.Column(db.Integer, db.ForeignKey('pagador.id'))
    pagador = db.relationship('Pagador', backref='pix')

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64))
    confirmado_por_pagador = db.Column(db.Boolean, default=False)
    confirmado_por_receptor = db.Column(db.Boolean, default=False)
    pagador_id = db.Column(db.Integer, db.ForeignKey('pagador.id'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    pagador = db.relationship('Pagador', backref='pagamentos')
    pedido = db.relationship('Pedido', backref='pagamentos')

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import Pessoa, Pagamento, Pedido
from app.forms import LoginForm, RegistrationForm
from functools import wraps

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Pessoa.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Pessoa(nome=form.nome.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/confirmar_pagamento_pagador/<int:pagamento_id>', methods=['POST'])
@login_required
def confirmar_pagamento_pagador(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    if pagamento and pagamento.pagador_id == current_user.id:
        pagamento.confirmado_por_pagador = True
        db.session.commit()
        flash('Pagamento confirmado pelo pagador.')
    return redirect(url_for('main.index'))

@bp.route('/confirmar_pagamento_receptor/<int:pagamento_id>', methods=['POST'])
@login_required
def confirmar_pagamento_receptor(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    pedido = Pedido.query.get(pagamento.pedido_id)
    if pedido and pedido.estabelecimento_id == current_user.estabelecimento_id:
        pagamento.confirmado_por_receptor = True
        db.session.commit()
        flash('Pagamento confirmado pelo receptor.')
    return redirect(url_for('main.index'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.permissao_id != 1:  # Assumindo que '1' é o ID de admin
            flash('Você não tem permissão para acessar esta página.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')

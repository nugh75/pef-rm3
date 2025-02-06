from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.auth import LoginForm, ChangePasswordForm
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Il tuo account è stato disattivato. Contatta l\'amministratore.', 'error')
                return render_template('auth/login.html', form=form)
                
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            if user:
                flash('Password non corretta. Se hai dimenticato la password, contatta l\'amministratore per reimpostarla.', 'error')
            else:
                flash('Email non trovata. Verifica di aver inserito l\'email corretta o contatta l\'amministratore.', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logout effettuato con successo', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/force-logout')
def force_logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password cambiata con successo!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Password attuale non corretta', 'error')
    return render_template('auth/change_password.html', form=form)
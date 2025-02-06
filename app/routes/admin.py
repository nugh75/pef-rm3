from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.forms.user import UserForm
from app.utils.decorators import role_required
from app import db
from config.roles import ROLE_ADMIN

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
@login_required
@role_required(ROLE_ADMIN)
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_ADMIN)
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email già registrata.', 'error')
            return redirect(url_for('admin.add_user'))
            
        user = User(
            email=form.email.data,
            nome=form.nome.data,
            cognome=form.cognome.data,
            ruolo=form.ruolo.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Utente registrato con successo!', 'success')
        return redirect(url_for('admin.users'))
        
    return render_template('admin/add_user.html', form=form)

@admin_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_ADMIN)
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        if user.id == current_user.id and not form.is_active.data:
            flash('Non puoi disattivare il tuo account!', 'error')
            return redirect(url_for('admin.edit_user', id=id))
            
        user.email = form.email.data
        user.nome = form.nome.data
        user.cognome = form.cognome.data
        user.ruolo = form.ruolo.data
        user.is_active = form.is_active.data
        
        if form.password.data:
            user.set_password(form.password.data)
            
        db.session.commit()
        flash('Utente aggiornato con successo!', 'success')
        return redirect(url_for('admin.users'))
        
    return render_template('admin/edit_user.html', form=form, user=user)

@admin_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id != current_user.id:
        db.session.delete(user)
        db.session.commit()
        flash('Utente eliminato con successo!', 'success')
    else:
        flash('Non puoi eliminare il tuo account!', 'error')
    return redirect(url_for('admin.users')) 
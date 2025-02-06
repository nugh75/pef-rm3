from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.tutor import TutorCoordinatori, TutorCollaboratori
from app.models.dipartimento import Dipartimento
from app.utils.decorators import role_required
from config.roles import ROLE_ADMIN, ROLE_SEGRETERIA

tutor_bp = Blueprint('tutor', __name__)

@tutor_bp.route('/tutor_coordinatori')
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def tutor_coordinatori():
    """Lista dei tutor coordinatori"""
    try:
        tutor = TutorCoordinatori.query.order_by(TutorCoordinatori.cognome).all()
        return render_template('tutor/tutor_coordinatori.html', tutor=tutor)
    except Exception as e:
        flash(f'Errore nel caricamento dei tutor coordinatori: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@tutor_bp.route('/tutor_coordinatori/add', methods=['GET', 'POST'])
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def add_tutor_coordinatore():
    """Aggiunge un nuovo tutor coordinatore"""
    try:
        dipartimenti = Dipartimento.query.order_by(Dipartimento.nome).all()
        if request.method == 'POST':
            try:
                nuovo_tutor = TutorCoordinatori(
                    nome=request.form['nome'],
                    cognome=request.form['cognome'],
                    email=request.form['email'],
                    telefono=request.form.get('telefono'),
                    dipartimento_id=request.form.get('dipartimento_id')
                )
                db.session.add(nuovo_tutor)
                db.session.commit()
                flash('Tutor coordinatore aggiunto con successo!', 'success')
                return redirect(url_for('tutor.tutor_coordinatori'))
            except Exception as e:
                db.session.rollback()
                flash(f'Errore durante l\'aggiunta del tutor: {str(e)}', 'error')
        return render_template('tutor/add_tutor_coordinatore.html', dipartimenti=dipartimenti)
    except Exception as e:
        flash(f'Errore nel caricamento dei dipartimenti: {str(e)}', 'error')
        return redirect(url_for('tutor.tutor_coordinatori'))

@tutor_bp.route('/tutor_coordinatori/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def edit_tutor_coordinatore(id):
    """Modifica un tutor coordinatore esistente"""
    try:
        tutor = TutorCoordinatori.query.get_or_404(id)
        dipartimenti = Dipartimento.query.order_by(Dipartimento.nome).all()
        if request.method == 'POST':
            try:
                tutor.nome = request.form['nome']
                tutor.cognome = request.form['cognome']
                tutor.email = request.form['email']
                tutor.telefono = request.form.get('telefono')
                tutor.dipartimento_id = request.form.get('dipartimento_id')
                db.session.commit()
                flash('Tutor coordinatore aggiornato con successo!', 'success')
                return redirect(url_for('tutor.tutor_coordinatori'))
            except Exception as e:
                db.session.rollback()
                flash(f'Errore durante l\'aggiornamento del tutor: {str(e)}', 'error')
        return render_template('tutor/edit_tutor_coordinatore.html', tutor=tutor, dipartimenti=dipartimenti)
    except Exception as e:
        flash(f'Errore nel caricamento dei dati: {str(e)}', 'error')
        return redirect(url_for('tutor.tutor_coordinatori'))

@tutor_bp.route('/tutor_coordinatori/delete/<int:id>', methods=['POST'])
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def delete_tutor_coordinatore(id):
    """Elimina un tutor coordinatore"""
    try:
        tutor = TutorCoordinatori.query.get_or_404(id)
        db.session.delete(tutor)
        db.session.commit()
        flash('Tutor coordinatore eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione del tutor: {str(e)}', 'error')
    return redirect(url_for('tutor.tutor_coordinatori'))

# Route per i tutor collaboratori
@tutor_bp.route('/tutor_collaboratori')
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def tutor_collaboratori():
    """Lista dei tutor collaboratori"""
    try:
        tutor = TutorCollaboratori.query.order_by(TutorCollaboratori.cognome).all()
        return render_template('tutor/tutor_collaboratori.html', tutor=tutor)
    except Exception as e:
        flash(f'Errore nel caricamento dei tutor collaboratori: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@tutor_bp.route('/tutor_collaboratori/add', methods=['GET', 'POST'])
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def add_tutor_collaboratore():
    """Aggiunge un nuovo tutor collaboratore"""
    try:
        dipartimenti = Dipartimento.query.order_by(Dipartimento.nome).all()
        if request.method == 'POST':
            try:
                nuovo_tutor = TutorCollaboratori(
                    nome=request.form['nome'],
                    cognome=request.form['cognome'],
                    email=request.form['email'],
                    telefono=request.form.get('telefono'),
                    dipartimento_id=request.form.get('dipartimento_id')
                )
                db.session.add(nuovo_tutor)
                db.session.commit()
                flash('Tutor collaboratore aggiunto con successo!', 'success')
                return redirect(url_for('tutor.tutor_collaboratori'))
            except Exception as e:
                db.session.rollback()
                flash(f'Errore durante l\'aggiunta del tutor: {str(e)}', 'error')
        return render_template('tutor/add_tutor_collaboratore.html', dipartimenti=dipartimenti)
    except Exception as e:
        flash(f'Errore nel caricamento dei dipartimenti: {str(e)}', 'error')
        return redirect(url_for('tutor.tutor_collaboratori'))

@tutor_bp.route('/tutor_collaboratori/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def edit_tutor_collaboratore(id):
    """Modifica un tutor collaboratore esistente"""
    try:
        tutor = TutorCollaboratori.query.get_or_404(id)
        dipartimenti = Dipartimento.query.order_by(Dipartimento.nome).all()
        if request.method == 'POST':
            try:
                tutor.nome = request.form['nome']
                tutor.cognome = request.form['cognome']
                tutor.email = request.form['email']
                tutor.telefono = request.form.get('telefono')
                tutor.dipartimento_id = request.form.get('dipartimento_id')
                db.session.commit()
                flash('Tutor collaboratore aggiornato con successo!', 'success')
                return redirect(url_for('tutor.tutor_collaboratori'))
            except Exception as e:
                db.session.rollback()
                flash(f'Errore durante l\'aggiornamento del tutor: {str(e)}', 'error')
        return render_template('tutor/edit_tutor_collaboratore.html', tutor=tutor, dipartimenti=dipartimenti)
    except Exception as e:
        flash(f'Errore nel caricamento dei dati: {str(e)}', 'error')
        return redirect(url_for('tutor.tutor_collaboratori'))

@tutor_bp.route('/tutor_collaboratori/delete/<int:id>', methods=['POST'])
@login_required
@role_required([ROLE_ADMIN, ROLE_SEGRETERIA])
def delete_tutor_collaboratore(id):
    """Elimina un tutor collaboratore"""
    try:
        tutor = TutorCollaboratori.query.get_or_404(id)
        db.session.delete(tutor)
        db.session.commit()
        flash('Tutor collaboratore eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione del tutor: {str(e)}', 'error')
    return redirect(url_for('tutor.tutor_collaboratori'))
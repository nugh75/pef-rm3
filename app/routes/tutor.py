from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.models.tutor import TutorCoordinatori, TutorCollaboratori
from app.models.student import RegistroPresenzeTirocinioIndiretto, Studenti
from app.models.user import User
from app.forms.auth import DeleteTutorCollaboratoreForm
from app.utils.decorators import role_required
from app.utils.calculations import calcola_totali_studente, calcola_totali_tutor
from app import db
from config.roles import ROLE_TUTOR_COORDINATORE, ROLE_TUTOR_COLLABORATORE, ROLE_SEGRETERIA

tutor_bp = Blueprint('tutor', __name__)

@tutor_bp.route('/area_tutor_coordinatore')
@login_required
@role_required(ROLE_TUTOR_COORDINATORE)
def area_tutor_coordinatore():
    tirocini = RegistroPresenzeTirocinioIndiretto.query.filter_by(
        id_tutor_coordinatore=current_user.id
    ).all()
    
    studenti_ids = set(t.id_studente for t in tirocini)
    studenti = User.query.filter(User.id.in_(studenti_ids)).all()
    
    for studente in studenti:
        totali = calcola_totali_studente(studente.id)
        studente.ore_totali = totali['ore_tirocinio_indiretto']
        studente.cfu_totali = totali['cfu_tirocinio_indiretto']
        
    totali = calcola_totali_tutor(current_user.id)
    return render_template('tutor/area_tutor_coordinatore.html', 
                         studenti=studenti, 
                         **totali)

@tutor_bp.route('/tutor_coordinatori')
@login_required
@role_required(ROLE_SEGRETERIA)
def tutor_coordinatori():
    tutor = TutorCoordinatori.query.options(
        db.joinedload(TutorCoordinatori.dipartimento)
    ).all()
    return render_template('tutor/tutor_coordinatori.html', tutor=tutor)

@tutor_bp.route('/tutor_coordinatori/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_tutor_coordinatore():
    dipartimenti = Dipartimenti.query.all()
    if request.method == 'POST':
        try:
            nuovo_tutor = TutorCoordinatori(
                nome=request.form['nome'],
                cognome=request.form['cognome'],
                email=request.form['email'],
                telefono=request.form['telefono'],
                dipartimento_id=request.form['dipartimento']
            )
            db.session.add(nuovo_tutor)
            db.session.commit()
            flash('Tutor coordinatore aggiunto con successo!', 'success')
            return redirect(url_for('tutor.tutor_coordinatori'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiunta del tutor: {str(e)}', 'error')
            
    return render_template('tutor/add_tutor_coordinatore.html', dipartimenti=dipartimenti)

@tutor_bp.route('/tutor_coordinatori/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_tutor_coordinatore(id):
    tutor = TutorCoordinatori.query.get_or_404(id)
    dipartimenti = Dipartimenti.query.all()
    
    if request.method == 'POST':
        try:
            tutor.nome = request.form['nome']
            tutor.cognome = request.form['cognome']
            tutor.email = request.form['email']
            tutor.telefono = request.form['telefono']
            tutor.dipartimento_id = request.form['dipartimento']
            
            db.session.commit()
            flash('Tutor coordinatore aggiornato con successo!', 'success')
            return redirect(url_for('tutor.tutor_coordinatori'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento del tutor: {str(e)}', 'error')
            
    return render_template('tutor/edit_tutor_coordinatore.html', 
                         tutor=tutor, 
                         dipartimenti=dipartimenti)

@tutor_bp.route('/tutor_coordinatori/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tutor_coordinatore(id):
    try:
        tutor = TutorCoordinatori.query.get_or_404(id)
        db.session.delete(tutor)
        db.session.commit()
        flash('Tutor coordinatore eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione del tutor: {str(e)}', 'error')
    return redirect(url_for('tutor.tutor_coordinatori'))

# Gestione Tutor Collaboratori
@tutor_bp.route('/tutor_collaboratori')
@login_required
@role_required(ROLE_SEGRETERIA)
def tutor_collaboratori():
    tutor = TutorCollaboratori.query.options(
        db.joinedload(TutorCollaboratori.dipartimento)
    ).all()
    delete_form = DeleteTutorCollaboratoreForm()
    return render_template('tutor/tutor_collaboratori.html', 
                         tutor=tutor, 
                         form=delete_form)

# ... altre route per la gestione dei tutor collaboratori simili a quelle dei coordinatori 
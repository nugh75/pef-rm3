from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app.models.school import ScuoleAccreditate
from app.forms.entity import ScuolaForm
from app.utils.decorators import role_required
from app import db
from config.roles import ROLE_SEGRETERIA

school_bp = Blueprint('school', __name__)

@school_bp.route('/scuole_accreditate')
@login_required
@role_required(ROLE_SEGRETERIA)
def scuole_accreditate():
    try:
        scuole = ScuoleAccreditate.query.all()
        return render_template('school/scuole_accreditate.html', scuole=scuole)
    except Exception as e:
        flash(f'Errore nel caricamento delle scuole: {str(e)}', 'error')
        return redirect(url_for('index'))

@school_bp.route('/scuole_accreditate/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_scuola():
    form = ScuolaForm()
    if form.validate_on_submit():
        try:
            nuova_scuola = ScuoleAccreditate(
                nome_scuola=form.nome_scuola.data,
                indirizzo=form.indirizzo.data,
                referente=form.referente.data,
                email_referente=form.email_referente.data
            )
            db.session.add(nuova_scuola)
            db.session.commit()
            flash('Scuola accreditata aggiunta con successo!', 'success')
            return redirect(url_for('school.scuole_accreditate'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiunta della scuola: {str(e)}', 'error')
    
    return render_template('school/add_scuola.html', form=form)

@school_bp.route('/scuole_accreditate/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_scuola(id):
    scuola = ScuoleAccreditate.query.get_or_404(id)
    form = ScuolaForm(obj=scuola)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(scuola)
            db.session.commit()
            flash('Scuola aggiornata con successo!', 'success')
            return redirect(url_for('school.scuole_accreditate'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento della scuola: {str(e)}', 'error')
    
    return render_template('school/edit_scuola.html', form=form, scuola=scuola)

@school_bp.route('/scuole_accreditate/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_scuola(id):
    try:
        scuola = ScuoleAccreditate.query.get_or_404(id)
        db.session.delete(scuola)
        db.session.commit()
        flash('Scuola accreditata eliminata con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione della scuola: {str(e)}', 'error')
    return redirect(url_for('school.scuole_accreditate'))

@school_bp.route('/get_tutor_esterno/<int:id_studente>')
@login_required
def get_tutor_esterno(id_studente):
    from app.models.student import Studenti
    studente = Studenti.query.get_or_404(id_studente)
    return {'tutor_esterno': studente.tutor_esterno if studente.tutor_esterno else ''} 
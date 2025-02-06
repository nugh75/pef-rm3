from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.school import ScuoleAccreditate
from app.utils.decorators import role_required
from app import db
from config.roles import ROLE_SEGRETERIA

school_bp = Blueprint('school', __name__)

@school_bp.route('/scuole_accreditate')
@login_required
@role_required(ROLE_SEGRETERIA)
def scuole_accreditate():
    """Lista delle scuole accreditate"""
    try:
        scuole = ScuoleAccreditate.query.order_by(ScuoleAccreditate.nome_scuola).all()
        return render_template('school/scuole_accreditate.html', scuole=scuole)
    except Exception as e:
        flash(f'Errore nel caricamento delle scuole: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@school_bp.route('/scuole_accreditate/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_scuola_accreditata():
    """Aggiunge una nuova scuola accreditata"""
    if request.method == 'POST':
        try:
            nuova_scuola = ScuoleAccreditate(
                nome_scuola=request.form['nome_scuola'],
                indirizzo=request.form['indirizzo'],
                referente=request.form['referente'],
                email_referente=request.form['email_referente']
            )
            db.session.add(nuova_scuola)
            db.session.commit()
            flash('Scuola accreditata aggiunta con successo!', 'success')
            return redirect(url_for('school.scuole_accreditate'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiunta della scuola: {str(e)}', 'error')
    return render_template('school/add_scuola.html')

@school_bp.route('/scuole_accreditate/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_scuola_accreditata(id):
    """Modifica una scuola accreditata esistente"""
    scuola = ScuoleAccreditate.query.get_or_404(id)
    if request.method == 'POST':
        try:
            scuola.nome_scuola = request.form['nome_scuola']
            scuola.indirizzo = request.form['indirizzo']
            scuola.referente = request.form['referente']
            scuola.email_referente = request.form['email_referente']
            db.session.commit()
            flash('Scuola aggiornata con successo!', 'success')
            return redirect(url_for('school.scuole_accreditate'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento della scuola: {str(e)}', 'error')
    return render_template('school/edit_scuola.html', scuola=scuola)

@school_bp.route('/scuole_accreditate/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_scuola_accreditata(id):
    """Elimina una scuola accreditata"""
    try:
        scuola = ScuoleAccreditate.query.get_or_404(id)
        db.session.delete(scuola)
        db.session.commit()
        flash('Scuola accreditata eliminata con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione della scuola: {str(e)}', 'error')
    return redirect(url_for('school.scuole_accreditate'))
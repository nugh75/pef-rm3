from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.models.student import RegistroPresenzeTirocinioIndiretto, RegistroPresenzeTirocinioDiretto, Studenti
from app.models.tutor import TutorCoordinatori
from app.models.school import ScuoleAccreditate
from app.forms.tirocinio import TirocinioDirettoForm, TirocinioIndirettoForm
from sqlalchemy import or_
from config.roles import ROLE_SEGRETERIA
from app import db

def calcola_cfu(ore, ore_per_cfu=6):
    """Calcola i CFU in base alle ore"""
    return round(ore / ore_per_cfu, 2) if ore else 0

segreteria_bp = Blueprint('segreteria', __name__)

@segreteria_bp.route('/dashboard')
@login_required
@role_required(ROLE_SEGRETERIA)
def dashboard():
    """Dashboard principale della segreteria"""
    return render_template('segreteria/dashboard.html')

@segreteria_bp.route('/tirocinio-diretto')
@login_required
@role_required(ROLE_SEGRETERIA)
def tirocinio_diretto():
    """Visualizza e gestisce il registro del tirocinio diretto"""
    query = RegistroPresenzeTirocinioDiretto.query.join(
        Studenti, RegistroPresenzeTirocinioDiretto.id_studente == Studenti.id_studente
    ).join(
        ScuoleAccreditate, RegistroPresenzeTirocinioDiretto.id_scuola == ScuoleAccreditate.id_scuola
    )

    # Filtri
    studente = request.args.get('studente', '').strip()
    scuola = request.args.get('scuola', '').strip()

    if studente:
        for parte in studente.split():
            query = query.filter(or_(
                Studenti.nome.ilike(f'%{parte}%'),
                Studenti.cognome.ilike(f'%{parte}%')
            ))

    if scuola:
        query = query.filter(ScuoleAccreditate.nome_scuola.ilike(f'%{scuola}%'))

    tirocini = query.order_by(RegistroPresenzeTirocinioDiretto.data.desc()).all()
    return render_template('segreteria/tirocinio_diretto.html', 
                         tirocini=tirocini,
                         studente=studente,
                         scuola=scuola)

@segreteria_bp.route('/tirocinio-diretto/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_tirocinio_diretto():
    """Aggiunge un nuovo tirocinio diretto"""
    form = TirocinioDirettoForm()
    form.id_studente.choices = [(s.id_studente, f"{s.cognome} {s.nome}") for s in Studenti.query.order_by(Studenti.cognome).all()]
    form.id_scuola.choices = [(s.id_scuola, s.nome_scuola) for s in ScuoleAccreditate.query.order_by(ScuoleAccreditate.nome_scuola).all()]

    if form.validate_on_submit():
        try:
            tirocinio = RegistroPresenzeTirocinioDiretto(
                id_studente=form.id_studente.data,
                id_scuola=form.id_scuola.data,
                tutor_esterno=form.tutor_esterno.data,
                data=form.data.data,
                ore=form.ore.data,
                cfu=calcola_cfu(form.ore.data),
                descrizione_attivita=form.descrizione_attivita.data
            )
            db.session.add(tirocinio)
            db.session.commit()
            flash('Tirocinio diretto aggiunto con successo!', 'success')
            return redirect(url_for('segreteria.tirocinio_diretto'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiunta del tirocinio: {str(e)}', 'error')

    return render_template('segreteria/form_tirocinio_diretto.html', form=form, title="Nuovo Tirocinio Diretto")

@segreteria_bp.route('/tirocinio-diretto/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_tirocinio_diretto(id):
    """Modifica un tirocinio diretto esistente"""
    tirocinio = RegistroPresenzeTirocinioDiretto.query.get_or_404(id)
    form = TirocinioDirettoForm(obj=tirocinio)
    form.id_studente.choices = [(s.id_studente, f"{s.cognome} {s.nome}") for s in Studenti.query.order_by(Studenti.cognome).all()]
    form.id_scuola.choices = [(s.id_scuola, s.nome_scuola) for s in ScuoleAccreditate.query.order_by(ScuoleAccreditate.nome_scuola).all()]

    if form.validate_on_submit():
        try:
            tirocinio.id_studente = form.id_studente.data
            tirocinio.id_scuola = form.id_scuola.data
            tirocinio.tutor_esterno = form.tutor_esterno.data
            tirocinio.data = form.data.data
            tirocinio.ore = form.ore.data
            tirocinio.cfu = calcola_cfu(form.ore.data)
            tirocinio.descrizione_attivita = form.descrizione_attivita.data
            db.session.commit()
            flash('Tirocinio diretto aggiornato con successo!', 'success')
            return redirect(url_for('segreteria.tirocinio_diretto'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento del tirocinio: {str(e)}', 'error')

    return render_template('segreteria/form_tirocinio_diretto.html', form=form, title="Modifica Tirocinio Diretto")

@segreteria_bp.route('/tirocinio-diretto/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tirocinio_diretto(id):
    """Elimina un tirocinio diretto"""
    tirocinio = RegistroPresenzeTirocinioDiretto.query.get_or_404(id)
    try:
        db.session.delete(tirocinio)
        db.session.commit()
        flash('Tirocinio diretto eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione del tirocinio: {str(e)}', 'error')
    return redirect(url_for('segreteria.tirocinio_diretto'))

@segreteria_bp.route('/tirocinio-indiretto')
@login_required
@role_required(ROLE_SEGRETERIA)
def tirocinio_indiretto():
    """Visualizza e gestisce il registro del tirocinio indiretto"""
    query = RegistroPresenzeTirocinioIndiretto.query.join(
        Studenti, RegistroPresenzeTirocinioIndiretto.id_studente == Studenti.id_studente
    ).outerjoin(
        TutorCoordinatori, RegistroPresenzeTirocinioIndiretto.id_tutor_coordinatore == TutorCoordinatori.id_tutor_coordinatore
    )

    # Filtri
    studente = request.args.get('studente', '').strip()
    tutor = request.args.get('tutor', '').strip()

    if studente:
        for parte in studente.split():
            query = query.filter(or_(
                Studenti.nome.ilike(f'%{parte}%'),
                Studenti.cognome.ilike(f'%{parte}%')
            ))

    if tutor:
        for parte in tutor.split():
            query = query.filter(or_(
                TutorCoordinatori.nome.ilike(f'%{parte}%'),
                TutorCoordinatori.cognome.ilike(f'%{parte}%')
            ))

    tirocini = query.order_by(RegistroPresenzeTirocinioIndiretto.data.desc()).all()
    return render_template('segreteria/tirocinio_indiretto.html',
                         tirocini=tirocini,
                         studente=studente,
                         tutor=tutor)

@segreteria_bp.route('/tirocinio-indiretto/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_tirocinio_indiretto():
    """Aggiunge un nuovo tirocinio indiretto"""
    form = TirocinioIndirettoForm()
    form.id_studente.choices = [(s.id_studente, f"{s.cognome} {s.nome}") for s in Studenti.query.order_by(Studenti.cognome).all()]
    form.id_tutor_coordinatore.choices = [(t.id_tutor_coordinatore, f"{t.cognome} {t.nome}") for t in TutorCoordinatori.query.order_by(TutorCoordinatori.cognome).all()]

    if form.validate_on_submit():
        try:
            tirocinio = RegistroPresenzeTirocinioIndiretto(
                id_studente=form.id_studente.data,
                id_tutor_coordinatore=form.id_tutor_coordinatore.data,
                data=form.data.data,
                ore=form.ore.data,
                cfu=calcola_cfu(form.ore.data),
                descrizione_attivita=form.descrizione_attivita.data
            )
            db.session.add(tirocinio)
            db.session.commit()
            flash('Tirocinio indiretto aggiunto con successo!', 'success')
            return redirect(url_for('segreteria.tirocinio_indiretto'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiunta del tirocinio: {str(e)}', 'error')

    return render_template('segreteria/form_tirocinio_indiretto.html', form=form, title="Nuovo Tirocinio Indiretto")

@segreteria_bp.route('/tirocinio-indiretto/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_tirocinio_indiretto(id):
    """Modifica un tirocinio indiretto esistente"""
    tirocinio = RegistroPresenzeTirocinioIndiretto.query.get_or_404(id)
    form = TirocinioIndirettoForm(obj=tirocinio)
    form.id_studente.choices = [(s.id_studente, f"{s.cognome} {s.nome}") for s in Studenti.query.order_by(Studenti.cognome).all()]
    form.id_tutor_coordinatore.choices = [(t.id_tutor_coordinatore, f"{t.cognome} {t.nome}") for t in TutorCoordinatori.query.order_by(TutorCoordinatori.cognome).all()]

    if form.validate_on_submit():
        try:
            tirocinio.id_studente = form.id_studente.data
            tirocinio.id_tutor_coordinatore = form.id_tutor_coordinatore.data
            tirocinio.data = form.data.data
            tirocinio.ore = form.ore.data
            tirocinio.cfu = calcola_cfu(form.ore.data)
            tirocinio.descrizione_attivita = form.descrizione_attivita.data
            db.session.commit()
            flash('Tirocinio indiretto aggiornato con successo!', 'success')
            return redirect(url_for('segreteria.tirocinio_indiretto'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento del tirocinio: {str(e)}', 'error')

    return render_template('segreteria/form_tirocinio_indiretto.html', form=form, title="Modifica Tirocinio Indiretto")

@segreteria_bp.route('/tirocinio-indiretto/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tirocinio_indiretto(id):
    """Elimina un tirocinio indiretto"""
    tirocinio = RegistroPresenzeTirocinioIndiretto.query.get_or_404(id)
    try:
        db.session.delete(tirocinio)
        db.session.commit()
        flash('Tirocinio indiretto eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione del tirocinio: {str(e)}', 'error')
    return redirect(url_for('segreteria.tirocinio_indiretto'))
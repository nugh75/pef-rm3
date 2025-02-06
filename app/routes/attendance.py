from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.attendance import Presenze
from app.models.student import Studenti
from app.models.course import Lezioni, Dipartimenti, ClassiConcorso, Percorsi
from app.forms.entity import PresenzaForm
from app.utils.decorators import role_required
from app import db
from config.roles import ROLE_SEGRETERIA
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/presenze')
@login_required
@role_required(ROLE_SEGRETERIA)
def lista_presenze():
    query = Presenze.query.join(Presenze.lezione).join(Presenze.studente)
    
    # Filtri
    if request.args.get('studente'):
        query = query.filter(Presenze.id_studente == request.args.get('studente'))
    if request.args.get('lezione'):
        query = query.filter(Presenze.id_lezione == request.args.get('lezione'))
    if request.args.get('data'):
        query = query.filter(Lezioni.data == datetime.strptime(request.args.get('data'), '%Y-%m-%d').date())
    if request.args.get('dipartimento'):
        query = query.join(Lezioni.dipartimenti).filter(Dipartimenti.id == request.args.get('dipartimento'))
    if request.args.get('classe_concorso'):
        query = query.join(Lezioni.classi_concorso).filter(ClassiConcorso.id_classe == request.args.get('classe_concorso'))
    if request.args.get('percorso'):
        query = query.join(Lezioni.percorsi).filter(Percorsi.id_percorso == request.args.get('percorso'))

    presenze = query.all()
    
    # Dati per i filtri
    studenti = Studenti.query.all()
    lezioni = Lezioni.query.all()
    dipartimenti = Dipartimenti.query.all()
    classi_concorso = ClassiConcorso.query.all()
    percorsi = Percorsi.query.order_by(Percorsi.nome_percorso).all()
    
    return render_template('attendance/lista_presenze.html',
                         presenze=presenze,
                         studenti=studenti,
                         lezioni=lezioni,
                         dipartimenti=dipartimenti,
                         classi_concorso=classi_concorso,
                         percorsi=percorsi)

@attendance_bp.route('/inserisci_presenza', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def inserisci_presenza():
    form = PresenzaForm()
    
    # Popola le scelte dei SelectField
    form.lezione.choices = [(l.id_lezione, f"{l.nome_lezione} - {l.data}") 
                           for l in Lezioni.query.order_by(Lezioni.data.desc()).all()]
    form.studente.choices = [(s.id_studente, f"{s.cognome} {s.nome}") 
                            for s in Studenti.query.order_by(Studenti.cognome).all()]
    
    if form.validate_on_submit():
        try:
            # Recupera la lezione per calcolare ore e CFU
            lezione = Lezioni.query.get_or_404(form.lezione.data)
            
            # Calcola ore dalla durata della lezione
            durata = lezione.durata
            ore = durata.hour + durata.minute/60 if durata else 0
            cfu = float(lezione.cfu) if lezione.cfu else 0
            
            # Verifica se esiste già una presenza
            presenza_esistente = Presenze.query.filter_by(
                id_lezione=form.lezione.data,
                id_studente=form.studente.data
            ).first()
            
            if not presenza_esistente:
                presenza = Presenze(
                    id_lezione=form.lezione.data,
                    id_studente=form.studente.data,
                    presente=form.presente.data,
                    ore=ore if form.presente.data else 0,
                    cfu=cfu if form.presente.data else 0,
                    note=form.note.data
                )
                db.session.add(presenza)
                db.session.commit()
                flash('Presenza registrata con successo!', 'success')
            else:
                flash('Presenza già registrata per questo studente in questa lezione.', 'error')
                
            return redirect(url_for('attendance.lista_presenze'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante la registrazione della presenza: {str(e)}', 'error')
    
    return render_template('attendance/inserisci_presenza.html', form=form)

@attendance_bp.route('/elimina_presenza/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def elimina_presenza(id):
    try:
        presenza = Presenze.query.get_or_404(id)
        db.session.delete(presenza)
        db.session.commit()
        flash('Presenza eliminata con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione: {str(e)}', 'error')
    return redirect(url_for('attendance.lista_presenze')) 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.models.course import (Lezioni, LezioniClassiConcorso, LezioniDipartimenti, 
                             LezioniPercorsi, ClassiConcorso, Dipartimenti, Percorsi)
from app.models.teacher import Insegnanti
from app.forms.entity import LezioneForm
from app.forms.imports import ImportLezioniForm
from app.utils.decorators import role_required
from app.utils.calculations import calcola_durata_e_cfu, calcola_totali_professore
from app import db
from config.roles import ROLE_PROFESSORE, ROLE_SEGRETERIA
from datetime import datetime
import pandas as pd

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/area_professore')
@login_required
@role_required(ROLE_PROFESSORE)
def area_professore():
    insegnante = Insegnanti.query.filter_by(email=current_user.email).first()
    if not insegnante:
        flash('Profilo insegnante non trovato', 'error')
        return redirect(url_for('main.index'))
        
    lezioni = Lezioni.query.filter_by(id_insegnante=insegnante.id_insegnante).all()
    totali = calcola_totali_professore(insegnante.id_insegnante)
    return render_template('teacher/area_professore.html', lezioni=lezioni, **totali)

@teacher_bp.route('/lezioni')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def lezioni():
    try:
        query = Lezioni.query.join(Lezioni.insegnante)
        
        # Se è un professore, mostra solo le sue lezioni
        if current_user.ruolo == ROLE_PROFESSORE:
            insegnante = Insegnanti.query.filter_by(email=current_user.email).first()
            if insegnante:
                query = query.filter(Lezioni.id_insegnante == insegnante.id_insegnante)
            else:
                flash('Profilo insegnante non trovato', 'error')
                return redirect(url_for('index'))
        
        # Filtri
        if request.args.get('nome'):
            query = query.filter(Lezioni.nome_lezione.ilike(f"%{request.args.get('nome')}%"))
        if request.args.get('insegnante'):
            query = query.filter(Lezioni.id_insegnante == request.args.get('insegnante'))
        if request.args.get('data'):
            query = query.filter(Lezioni.data == datetime.strptime(request.args.get('data'), '%Y-%m-%d').date())
        if request.args.get('orario'):
            query = query.filter(Lezioni.orario_inizio >= datetime.strptime(request.args.get('orario'), '%H:%M').time())
        if request.args.getlist('classe'):
            query = query.join(Lezioni.classi_concorso).filter(ClassiConcorso.id_classe.in_(request.args.getlist('classe')))
        if request.args.getlist('dipartimento'):
            query = query.join(Lezioni.dipartimenti).filter(Dipartimenti.id.in_(request.args.getlist('dipartimento')))
        if request.args.getlist('percorso'):
            query = query.join(Lezioni.percorsi).filter(Percorsi.id_percorso.in_(request.args.getlist('percorso')))
            
        query = query.distinct()
        lezioni_list = query.all()
        cfu_sum = sum(float(l.cfu) if l.cfu else 0 for l in lezioni_list)
        
        # Dati per i filtri
        tutti_insegnanti = Insegnanti.query.order_by(Insegnanti.cognome).all()
        tutte_classi = ClassiConcorso.query.order_by(ClassiConcorso.nome_classe).all()
        dipartimenti = Dipartimenti.query.order_by(Dipartimenti.nome).all()
        percorsi = Percorsi.query.order_by(Percorsi.nome_percorso).all()
        
        return render_template('teacher/lezioni.html',
                             lezioni=lezioni_list,
                             tutti_insegnanti=tutti_insegnanti,
                             tutte_classi=tutte_classi,
                             dipartimenti=dipartimenti,
                             percorsi=percorsi,
                             cfu_sum=cfu_sum)
                             
    except Exception as e:
        flash(f'Si è verificato un errore nel caricamento delle lezioni: {str(e)}', 'error')
        return redirect(url_for('teacher.area_professore'))

@teacher_bp.route('/add_lezione', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def add_lezione():
    try:
        if current_user.ruolo == ROLE_PROFESSORE:
            insegnante = Insegnanti.query.filter_by(email=current_user.email).first()
            if not insegnante:
                flash('Profilo insegnante non trovato', 'error')
                return redirect(url_for('teacher.lezioni'))
            id_insegnante = insegnante.id_insegnante
        else:
            primo_insegnante = Insegnanti.query.first()
            id_insegnante = primo_insegnante.id_insegnante if primo_insegnante else None
            
        orario_inizio = datetime.strptime('09:00', '%H:%M').time()
        orario_fine = datetime.strptime('11:00', '%H:%M').time()
        durata, cfu = calcola_durata_e_cfu(orario_inizio, orario_fine)
        
        nuova_lezione = Lezioni(
            nome_lezione="Nuova Lezione",
            data=datetime.now().date(),
            orario_inizio=orario_inizio,
            orario_fine=orario_fine,
            durata=durata,
            cfu=cfu,
            id_insegnante=id_insegnante
        )
        
        db.session.add(nuova_lezione)
        db.session.commit()
        
        flash('Nuova lezione creata! Modifica i dettagli.', 'success')
        return redirect(url_for('teacher.edit_lezione', id=nuova_lezione.id_lezione))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante la creazione della lezione: {str(e)}', 'error')
        return redirect(url_for('teacher.lezioni'))

@teacher_bp.route('/edit_lezione/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def edit_lezione(id):
    lezione = Lezioni.query.get_or_404(id)
    form = LezioneForm(obj=lezione)
    
    # Popola le scelte dei SelectField
    form.insegnante.choices = [(i.id_insegnante, f"{i.cognome} {i.nome}") 
                              for i in Insegnanti.query.order_by(Insegnanti.cognome).all()]
    form.classi_concorso.choices = [(c.id_classe, f"{c.nome_classe} - {c.denominazione_classe}") 
                                   for c in ClassiConcorso.query.order_by(ClassiConcorso.nome_classe).all()]
    form.dipartimenti.choices = [(d.id, d.nome) 
                                for d in Dipartimenti.query.order_by(Dipartimenti.nome).all()]
    form.percorsi.choices = [(p.id_percorso, p.nome_percorso) 
                            for p in Percorsi.query.order_by(Percorsi.nome_percorso).all()]
    
    if form.validate_on_submit():
        try:
            # Aggiorna i dati base
            lezione.nome_lezione = form.nome_lezione.data
            lezione.data = form.data.data
            lezione.orario_inizio = form.orario_inizio.data
            lezione.orario_fine = form.orario_fine.data
            lezione.id_insegnante = form.insegnante.data
            
            # Calcola durata e CFU
            durata, cfu = calcola_durata_e_cfu(form.orario_inizio.data, form.orario_fine.data)
            lezione.durata = durata
            lezione.cfu = cfu
            
            # Aggiorna le relazioni
            if form.classi_concorso.data:
                classe = ClassiConcorso.query.get(form.classi_concorso.data)
                if classe:
                    lezione.classi_concorso = [classe]
            if form.dipartimenti.data:
                dipartimento = Dipartimenti.query.get(form.dipartimenti.data)
                if dipartimento:
                    lezione.dipartimenti = [dipartimento]
            if form.percorsi.data:
                percorso = Percorsi.query.get(form.percorsi.data)
                if percorso:
                    lezione.percorsi = [percorso]
            
            db.session.commit()
            flash('Lezione aggiornata con successo!', 'success')
            return redirect(url_for('teacher.lezioni'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento della lezione: {str(e)}', 'error')
            
    return render_template('teacher/edit_lezione.html', form=form, lezione=lezione)

@teacher_bp.route('/delete_lezione/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def delete_lezione(id):
    try:
        lezione = Lezioni.query.get_or_404(id)
        db.session.delete(lezione)
        db.session.commit()
        flash('Lezione eliminata con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Errore durante l\'eliminazione della lezione: {str(e)}', 'error')
    return redirect(url_for('teacher.lezioni'))

@teacher_bp.route('/import_lezioni', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def import_lezioni():
    form = ImportLezioniForm()
    results = None
    
    if form.validate_on_submit():
        try:
            file = form.file.data
            if file and allowed_file(file.filename):
                # Leggi il file Excel
                df = pd.read_excel(file, engine='openpyxl')
                
                # Valida i dati
                valid_lessons, validation_errors = validate_excel_data(df)
                
                if validation_errors:
                    results = {'success': [], 'errors': validation_errors}
                else:
                    # Importa le lezioni valide
                    success, import_errors = import_lessons(valid_lessons)
                    results = {
                        'success': success,
                        'errors': import_errors
                    }
                    
                    if success and not import_errors:
                        flash('Importazione completata con successo!', 'success')
                    elif success:
                        flash('Importazione completata con alcuni errori.', 'warning')
                    else:
                        flash('Errore durante l\'importazione.', 'error')
            else:
                flash('Tipo di file non supportato.', 'error')
        except Exception as e:
            flash(f'Errore durante l\'elaborazione del file: {str(e)}', 'error')
    
    return render_template('teacher/import_lezioni.html', form=form, results=results) 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.models.student import (Studenti, RegistroPresenzeTirocinioDiretto, 
                              RegistroPresenzeTirocinioIndiretto)
from app.models.school import ScuoleAccreditate
from app.models.tutor import TutorCoordinatori
from app.forms.imports import ImportTirocinioDirettoForm, ImportTirocinioIndirettoForm
from app.utils.decorators import role_required
from app.utils.calculations import calcola_totali_studente, calcola_cfu
from app import db
from config.roles import ROLE_STUDENTE, ROLE_SEGRETERIA
import pandas as pd
from datetime import datetime

student_bp = Blueprint('student', __name__)

@student_bp.route('/area_studente')
@login_required
@role_required(ROLE_STUDENTE)
def area_studente():
    totali = calcola_totali_studente(current_user.id)
    totale_cfu = totali['cfu_tirocinio_diretto'] + totali['cfu_tirocinio_indiretto']
    return render_template('student/area_studente.html', totale_cfu=totale_cfu, **totali)

@student_bp.route('/tirocinio_diretto')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def tirocinio_diretto():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    query = db.session.query(
        RegistroPresenzeTirocinioDiretto,
        Studenti.nome.label('studente_nome'),
        Studenti.cognome.label('studente_cognome'),
        ScuoleAccreditate.nome_scuola.label('scuola_nome')
    ).join(
        Studenti, 
        RegistroPresenzeTirocinioDiretto.id_studente == Studenti.id_studente
    ).join(
        ScuoleAccreditate, 
        RegistroPresenzeTirocinioDiretto.id_scuola == ScuoleAccreditate.id_scuola
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

    tirocini = query.all()
    cfu_sum = sum(t[0].cfu for t in tirocini if t[0].cfu)
    
    return render_template('student/tirocinio_diretto.html', 
                         tirocini=tirocini, 
                         studente=studente, 
                         scuola=scuola, 
                         cfu_sum=cfu_sum)

@student_bp.route('/tirocinio_indiretto')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def tirocinio_indiretto():
    query = db.session.query(
        RegistroPresenzeTirocinioIndiretto,
        Studenti.nome.label('studente_nome'),
        Studenti.cognome.label('studente_cognome'),
        TutorCoordinatori.nome.label('tutor_nome'),
        TutorCoordinatori.cognome.label('tutor_cognome')
    ).join(
        Studenti, 
        RegistroPresenzeTirocinioIndiretto.id_studente == Studenti.id_studente
    ).outerjoin(
        TutorCoordinatori, 
        RegistroPresenzeTirocinioIndiretto.id_tutor_coordinatore == TutorCoordinatori.id_tutor_coordinatore
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

    tirocini = query.all()
    cfu_sum = sum(t[0].cfu for t in tirocini if t[0].cfu)
    
    return render_template('student/tirocinio_indiretto.html', 
                         tirocini=tirocini, 
                         studente=studente, 
                         tutor=tutor, 
                         cfu_sum=cfu_sum)

# Altre route per la gestione dei tirocini... 
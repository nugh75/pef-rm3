from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.models.student import RegistroPresenzeTirocinioIndiretto, RegistroPresenzeTirocinioDiretto
from config.roles import ROLE_STUDENTE

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
@role_required(ROLE_STUDENTE)
def dashboard():
    """Dashboard principale dello studente"""
    # Calcola i totali per il tirocinio diretto
    tirocini_diretti = RegistroPresenzeTirocinioDiretto.query.filter_by(
        id_studente=current_user.id
    ).all()
    ore_tirocinio_diretto = sum(t.ore for t in tirocini_diretti if t.ore)
    cfu_tirocinio_diretto = sum(t.cfu for t in tirocini_diretti if t.cfu)

    # Calcola i totali per il tirocinio indiretto
    tirocini_indiretti = RegistroPresenzeTirocinioIndiretto.query.filter_by(
        id_studente=current_user.id
    ).all()
    ore_tirocinio_indiretto = sum(t.ore for t in tirocini_indiretti if t.ore)
    cfu_tirocinio_indiretto = sum(t.cfu for t in tirocini_indiretti if t.cfu)

    return render_template('studente/dashboard.html',
                         ore_tirocinio_diretto=ore_tirocinio_diretto,
                         cfu_tirocinio_diretto=cfu_tirocinio_diretto,
                         ore_tirocinio_indiretto=ore_tirocinio_indiretto,
                         cfu_tirocinio_indiretto=cfu_tirocinio_indiretto)

@student_bp.route('/registro_tirocinio_diretto')
@login_required
@role_required(ROLE_STUDENTE)
def registro_tirocinio_diretto():
    """Visualizza il registro del tirocinio diretto dello studente"""
    tirocini = RegistroPresenzeTirocinioDiretto.query.filter_by(
        id_studente=current_user.id
    ).order_by(RegistroPresenzeTirocinioDiretto.data.desc()).all()
    return render_template('studente/registro_tirocinio_diretto.html', tirocini=tirocini)

@student_bp.route('/registro_tirocinio_indiretto')
@login_required
@role_required(ROLE_STUDENTE)
def registro_tirocinio_indiretto():
    """Visualizza il registro del tirocinio indiretto dello studente"""
    tirocini = RegistroPresenzeTirocinioIndiretto.query.filter_by(
        id_studente=current_user.id
    ).order_by(RegistroPresenzeTirocinioIndiretto.data.desc()).all()
    return render_template('studente/registro_tirocinio_indiretto.html', tirocini=tirocini)
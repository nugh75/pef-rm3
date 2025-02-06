from flask import Blueprint, redirect, url_for
from flask_login import current_user
from config.roles import (ROLE_STUDENTE, ROLE_PROFESSORE, ROLE_SEGRETERIA, 
                         ROLE_TUTOR_COORDINATORE, ROLE_TUTOR_COLLABORATORE, ROLE_ADMIN)

# DEBUG: Print di debug
print("Definizione main_bp in main.py")
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    # Reindirizza in base al ruolo
    if current_user.ruolo == ROLE_STUDENTE:
        return redirect(url_for('student.area_studente'))
    elif current_user.ruolo == ROLE_PROFESSORE:
        return redirect(url_for('teacher.area_professore'))
    elif current_user.ruolo == ROLE_TUTOR_COORDINATORE:
        return redirect(url_for('tutor.area_tutor_coordinatore'))
    elif current_user.ruolo == ROLE_SEGRETERIA:
        return redirect(url_for('admin.users'))
    elif current_user.ruolo == ROLE_ADMIN:
        return redirect(url_for('admin.users'))
    else:
        return redirect(url_for('auth.login')) 
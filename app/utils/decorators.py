"""
Decoratori personalizzati per l'applicazione.
"""

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    """
    Decoratore per proteggere le route in base al ruolo dell'utente.
    
    Args:
        *roles: Lista di ruoli autorizzati ad accedere alla route
        
    Returns:
        Function: Decoratore che verifica il ruolo dell'utente
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Devi effettuare il login per accedere a questa pagina.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.ruolo not in roles:
                flash('Non hai i permessi necessari per accedere a questa pagina.', 'error')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator 
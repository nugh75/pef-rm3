"""
Decoratori personalizzati per l'applicazione.
"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user
from config.roles import ROLE_SEGRETERIA, ROLE_ADMIN

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
            # Permetti alla segreteria di accedere a tutte le pagine tranne quelle admin
            if current_user.ruolo == ROLE_SEGRETERIA and ROLE_ADMIN not in roles:
                return f(*args, **kwargs)
            # Per tutti gli altri ruoli, verifica normalmente i permessi
            elif current_user.ruolo not in roles:
                flash('Non hai i permessi necessari per accedere a questa pagina.', 'error')
                # Invece di reindirizzare a main.index, mostra una pagina 403
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
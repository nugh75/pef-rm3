"""
Funzioni di utilità per la gestione dei file.
"""

def allowed_file(filename):
    """
    Verifica se l'estensione del file è consentita.
    
    Args:
        filename (str): Nome del file da verificare
        
    Returns:
        bool: True se l'estensione è consentita, False altrimenti
    """
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'] 
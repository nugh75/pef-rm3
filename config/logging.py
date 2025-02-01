"""
Configurazione del logging per l'applicazione PEF-RM3.
Gestisce tutte le impostazioni relative al logging.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """
    Configura il sistema di logging per l'applicazione Flask.
    
    Args:
        app: L'istanza dell'applicazione Flask
        
    Returns:
        None
    """
    # Crea la directory logs se non esiste
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Configura il file handler con rotazione
    file_handler = RotatingFileHandler(
        'logs/pef-rm3.log',
        maxBytes=10240,  # 10KB per file
        backupCount=10   # Mantiene fino a 10 file di backup
    )
    
    # Imposta il formato del log
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    # Imposta il livello di logging
    file_handler.setLevel(logging.INFO)
    
    # Aggiungi l'handler all'app
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log iniziale dell'avvio dell'applicazione
    app.logger.info('PEF-RM3 startup')

def get_logger(name):
    """
    Crea e restituisce un logger configurato per un modulo specifico.
    
    Args:
        name: Nome del logger (tipicamente __name__ del modulo)
        
    Returns:
        logging.Logger: Logger configurato
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evita di aggiungere handler duplicati
    if not logger.handlers:
        handler = RotatingFileHandler(
            'logs/pef-rm3.log',
            maxBytes=10240,
            backupCount=10
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        logger.addHandler(handler)
    
    return logger
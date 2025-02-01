"""
Configurazione generale per l'applicazione PEF-RM3.
Centralizza tutte le configurazioni dell'applicazione.
"""

import os
from dotenv import load_dotenv
from .database import Database
from .logging import configure_logging

# Carica le variabili d'ambiente
load_dotenv()

class Config:
    """Classe per gestire la configurazione generale dell'applicazione."""
    
    # Chiave segreta per le sessioni
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # Configurazioni del database
    SQLALCHEMY_DATABASE_URI = Database.get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurazione upload file
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configurazione sessione
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minuti
    
    @classmethod
    def init_app(cls, app):
        """
        Inizializza l'applicazione con tutte le configurazioni necessarie.
        
        Args:
            app: L'istanza dell'applicazione Flask
            
        Returns:
            None
        """
        # Configura il logging
        configure_logging(app)
        
        # Assicurati che la cartella uploads esista
        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER)
        
        # Configura l'app
        app.config.from_object(cls)
        
        return app

class DevelopmentConfig(Config):
    """Configurazione per l'ambiente di sviluppo."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configurazione per l'ambiente di test."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usa un database SQLite in memoria per i test

class ProductionConfig(Config):
    """Configurazione per l'ambiente di produzione."""
    DEBUG = False
    TESTING = False
    
    @classmethod
    def init_app(cls, app):
        """
        Inizializza l'applicazione per l'ambiente di produzione.
        Aggiunge configurazioni specifiche per la produzione.
        """
        super().init_app(app)
        
        # Configurazioni aggiuntive per la produzione
        # Ad esempio, configurazione per logging su file di produzione
        import logging
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            'logs/production.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

# Dizionario per mappare gli ambienti alle relative configurazioni
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
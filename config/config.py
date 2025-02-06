"""
Configurazione generale per l'applicazione PEF-RM3.
Centralizza tutte le configurazioni dell'applicazione.
"""

import os
from dotenv import load_dotenv
from .database import Database
from .logging import configure_logging
from datetime import timedelta

# Carica le variabili d'ambiente
load_dotenv()

class Config:
    """Classe per gestire la configurazione generale dell'applicazione."""
    
    # Configurazione base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chiave-segreta-di-default'
    SQLALCHEMY_DATABASE_URI = Database.get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurazione upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Configurazione sessione
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def init_app(app):
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
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        # Configura l'app
        app.config.from_object(Config)
        
        return app

class DevelopmentConfig(Config):
    """Configurazione per l'ambiente di sviluppo."""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev-database.sqlite'
    
    # Override per sviluppo
    SESSION_COOKIE_SECURE = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log configurazione di sviluppo
        app.logger.info('*** MODALITÀ SVILUPPO ***')
        app.logger.info(f'Database: {cls.SQLALCHEMY_DATABASE_URI}')

class TestingConfig(Config):
    """Configurazione per l'ambiente di test."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///test-database.sqlite'
    WTF_CSRF_ENABLED = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        app.logger.info('*** MODALITÀ TEST ***')

class ProductionConfig(Config):
    """Configurazione per l'ambiente di produzione."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///production-database.sqlite'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configurazione logging di produzione
        import logging
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler('logs/application.log',
                                         maxBytes=10240,
                                         backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Applicazione avviata')

# Dizionario per mappare gli ambienti alle relative configurazioni
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
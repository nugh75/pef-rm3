"""
Configurazione del database per l'applicazione PEF-RM3.
Gestisce tutte le impostazioni relative al database.
"""

import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

class Database:
    """Classe per gestire la configurazione del database."""
    
    @staticmethod
    def get_database_uri():
        """
        Costruisce e restituisce l'URI del database dalle variabili d'ambiente.
        
        Returns:
            str: URI completo del database per SQLAlchemy
        """
        return (
            f"mysql+pymysql://"
            f"{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

    @staticmethod
    def get_config():
        """
        Restituisce la configurazione completa del database per Flask-SQLAlchemy.
        
        Returns:
            dict: Dizionario con tutte le configurazioni del database
        """
        return {
            'SQLALCHEMY_DATABASE_URI': Database.get_database_uri(),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            # Altre configurazioni del database possono essere aggiunte qui
        }

    @staticmethod
    def test_connection():
        """
        Verifica la connessione al database.
        
        Returns:
            bool: True se la connessione ha successo, False altrimenti
        """
        try:
            from sqlalchemy import create_engine
            engine = create_engine(Database.get_database_uri())
            connection = engine.connect()
            connection.close()
            return True
        except Exception as e:
            print(f"Errore di connessione al database: {str(e)}")
            return False
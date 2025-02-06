from app import create_app, db
from app.models.user import User
from config.roles import ROLE_ADMIN
import os

def init_db():
    app = create_app()
    with app.app_context():
        # Stampa il percorso del database
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        print(f"Inizializzazione database in: {db_path}")
        
        # Verifica se il file del database esiste
        if os.path.exists(db_path):
            print("Il file del database esiste già")
        else:
            print("Creazione nuovo file database")
            
        # Crea tutte le tabelle
        print("Creazione tabelle...")
        db.create_all()
        print("Tabelle create")
        
        # Elenca le tabelle create
        print("\nTabelle nel database:")
        for table in db.metadata.tables.keys():
            print(f"- {table}")
        
        # Verifica se esiste già un admin
        admin = User.query.filter_by(ruolo=ROLE_ADMIN).first()
        if not admin:
            print("\nCreazione utente admin...")
            # Crea un utente admin di default
            admin = User(
                email='admin@example.com',
                nome='Admin',
                cognome='Admin',
                ruolo=ROLE_ADMIN,
                is_active=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Utente admin creato con successo!")
        else:
            print("\nUtente admin già esistente")
        
        print("\nDatabase inizializzato con successo!")

if __name__ == '__main__':
    init_db() 
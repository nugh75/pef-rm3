from app import create_app
from app import db
import click

app = create_app()

@app.cli.command('create-tables')
def create_tables():
    """Crea tutte le tabelle nel database"""
    try:
        db.create_all()
        print('Tabelle create con successo!')
    except Exception as e:
        print(f'Errore durante la creazione delle tabelle: {e}')

@app.cli.command('create-admin')
def create_admin():
    """Crea il primo utente amministratore"""
    from app.models.user import User
    from config.roles import ROLE_ADMIN
    
    email = input('Email amministratore: ')
    password = input('Password: ')
    nome = input('Nome: ')
    cognome = input('Cognome: ')
    
    if User.query.filter_by(email=email).first():
        print('Email già registrata')
        return
        
    admin = User(email=email, nome=nome, cognome=cognome, ruolo=ROLE_ADMIN, is_active=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print('Amministratore creato con successo!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 
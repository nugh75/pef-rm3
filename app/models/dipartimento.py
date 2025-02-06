from app import db

class Dipartimento(db.Model):
    """Modello per i dipartimenti dell'università"""
    __tablename__ = 'Dipartimenti'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descrizione = db.Column(db.Text)
    
    # Relazioni
    tutor_coordinatori = db.relationship('TutorCoordinatori', backref='dipartimento', lazy=True)
    tutor_collaboratori = db.relationship('TutorCollaboratori', backref='dipartimento', lazy=True)

    def __init__(self, nome, descrizione=None):
        self.nome = nome
        self.descrizione = descrizione

    def __repr__(self):
        return f'<Dipartimento {self.nome}>'
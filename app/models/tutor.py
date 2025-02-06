from app import db
from datetime import datetime

class TutorBase(db.Model):
    """Classe base per i tutor con campi comuni"""
    __abstract__ = True

    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    dipartimento_id = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'))
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    data_modifica = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    attivo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.nome} {self.cognome}>'

class TutorCoordinatori(TutorBase):
    """Modello per i tutor coordinatori"""
    __tablename__ = 'TutorCoordinatori'
    __table_args__ = {'extend_existing': True}

    id_tutor_coordinatore = db.Column(db.Integer, primary_key=True)
    ore_disponibili = db.Column(db.Integer, default=0)
    specializzazione = db.Column(db.String(100))
    
    # Relazioni
    tirocini = db.relationship('RegistroPresenzeTirocinioIndiretto', 
                             backref='tutor_coordinatore', 
                             lazy=True)

    def __init__(self, nome, cognome, email, telefono=None, dipartimento_id=None,
                 ore_disponibili=0, specializzazione=None):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.telefono = telefono
        self.dipartimento_id = dipartimento_id
        self.ore_disponibili = ore_disponibili
        self.specializzazione = specializzazione

class TutorCollaboratori(TutorBase):
    """Modello per i tutor collaboratori"""
    __tablename__ = 'TutorCollaboratori'
    __table_args__ = {'extend_existing': True}

    id_tutor_collaboratore = db.Column(db.Integer, primary_key=True)
    area_competenza = db.Column(db.String(100))
    disponibilita_settimanale = db.Column(db.Integer, default=0)  # ore settimanali

    def __init__(self, nome, cognome, email, telefono=None, dipartimento_id=None,
                 area_competenza=None, disponibilita_settimanale=0):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.telefono = telefono
        self.dipartimento_id = dipartimento_id
        self.area_competenza = area_competenza
        self.disponibilita_settimanale = disponibilita_settimanale
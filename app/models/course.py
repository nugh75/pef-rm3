from app import db
from datetime import time

class Lezioni(db.Model):
    __tablename__ = 'Lezioni'
    id_lezione = db.Column(db.Integer, primary_key=True)
    nome_lezione = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    orario_inizio = db.Column(db.Time, nullable=False)
    orario_fine = db.Column(db.Time, nullable=False)
    durata = db.Column(db.Time, nullable=True)
    cfu = db.Column(db.Numeric(4,2), nullable=True)
    id_insegnante = db.Column(db.Integer, db.ForeignKey('Insegnanti.id_insegnante'), nullable=True)

    classi_concorso = db.relationship('ClassiConcorso',
                                    secondary='Lezioni_ClassiConcorso',
                                    backref=db.backref('lezioni_correlate', lazy='dynamic'))
    dipartimenti = db.relationship('Dipartimenti',
                                 secondary='Lezioni_Dipartimenti',
                                 backref=db.backref('lezioni_correlate', lazy='dynamic'))
    percorsi = db.relationship('Percorsi',
                             secondary='Lezioni_Percorsi',
                             backref=db.backref('lezioni_correlate', lazy='dynamic'))

class LezioniClassiConcorso(db.Model):
    __tablename__ = 'Lezioni_ClassiConcorso'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_classe = db.Column(db.Integer, db.ForeignKey('Classi di concorso.id_classe'), primary_key=True)

class LezioniDipartimenti(db.Model):
    __tablename__ = 'Lezioni_Dipartimenti'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_dipartimento = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), primary_key=True)

class LezioniPercorsi(db.Model):
    __tablename__ = 'Lezioni_Percorsi'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_percorso = db.Column(db.Integer, db.ForeignKey('Percorsi.id_percorso'), primary_key=True)

class ClassiConcorso(db.Model):
    __tablename__ = 'Classi di concorso'
    id_classe = db.Column(db.Integer, primary_key=True)
    dipartimento = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), nullable=False)
    nome_classe = db.Column(db.String(4), nullable=False)
    denominazione_classe = db.Column(db.String(255), nullable=False)

class Percorsi(db.Model):
    __tablename__ = 'Percorsi'
    id_percorso = db.Column(db.Integer, primary_key=True)
    nome_percorso = db.Column(db.String(255), nullable=False)

class Dipartimenti(db.Model):
    __tablename__ = 'Dipartimenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False) 
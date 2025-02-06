from app import db

class Presenze(db.Model):
    __tablename__ = 'RegistroPresenzeStudenti'
    id_presenza = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione', ondelete='CASCADE'), nullable=False)
    id_studente = db.Column(db.Integer, db.ForeignKey('Studenti.id_studente', ondelete='CASCADE'), nullable=False)
    presente = db.Column(db.Boolean, default=True, nullable=False)
    ore = db.Column(db.Float, default=0)
    cfu = db.Column(db.Float, default=0)
    note = db.Column(db.String(255))
    
    lezione = db.relationship('Lezioni', backref='presenze')
    studente = db.relationship('Studenti', backref='presenze') 
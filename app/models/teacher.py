from app import db

class Insegnanti(db.Model):
    __tablename__ = 'Insegnanti'
    id_insegnante = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    id_dipartimento = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'))
    id_ssd = db.Column(db.Integer, db.ForeignKey('SSD.id_ssd'))
    dipartimento = db.relationship('Dipartimenti', backref='insegnanti', lazy=True)
    lezioni = db.relationship('Lezioni', backref='insegnante', lazy=True)

class SSD(db.Model):
    __tablename__ = 'SSD'
    id_ssd = db.Column(db.Integer, primary_key=True)
    nome_ssd = db.Column(db.String(255), nullable=False)
    insegnanti = db.relationship('Insegnanti', backref='ssd', lazy=True) 
from app import db

class ScuoleAccreditate(db.Model):
    __tablename__ = 'ScuoleAccreditate'
    id_scuola = db.Column(db.Integer, primary_key=True)
    nome_scuola = db.Column(db.String(150), nullable=False)
    indirizzo = db.Column(db.String(255))
    referente = db.Column(db.String(100))
    email_referente = db.Column(db.String(150)) 
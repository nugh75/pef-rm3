from app import db

class TutorCoordinatori(db.Model):
    __tablename__ = 'TutorCoordinatori'
    id_tutor_coordinatore = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    dipartimento_id = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), nullable=True)
    dipartimento = db.relationship('Dipartimenti', backref='tutor_coordinatori', lazy=True)

class TutorCollaboratori(db.Model):
    __tablename__ = 'TutorCollaboratori'
    id_tutor_collaboratore = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    dipartimento_id = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), nullable=False)
    dipartimento = db.relationship('Dipartimenti', backref='tutor_collaboratori', lazy=True) 
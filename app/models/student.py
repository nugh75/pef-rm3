from app import db

class Studenti(db.Model):
    __tablename__ = 'Studenti'
    id_studente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(15))
    classe_id = db.Column(db.Integer, db.ForeignKey('Classi di concorso.id_classe'), nullable=False)
    percorso_id = db.Column(db.Integer, db.ForeignKey('Percorsi.id_percorso'), nullable=False)
    scuola_assegnata_id = db.Column(db.Integer, db.ForeignKey('ScuoleAccreditate.id_scuola'))
    tutor_esterno = db.Column(db.String(150))

    # Relazioni
    tirocini_diretti = db.relationship('RegistroPresenzeTirocinioDiretto', backref='studente', lazy=True)
    tirocini_indiretti = db.relationship('RegistroPresenzeTirocinioIndiretto', backref='studente', lazy=True)

class RegistroPresenzeTirocinioDiretto(db.Model):
    __tablename__ = 'RegistroPresenzeTirocinioDiretto'
    id_tirocinio_diretto = db.Column(db.Integer, primary_key=True)
    id_studente = db.Column(db.Integer, db.ForeignKey('Studenti.id_studente'), nullable=False)
    id_scuola = db.Column(db.Integer, db.ForeignKey('ScuoleAccreditate.id_scuola'), nullable=False)
    tutor_esterno = db.Column(db.String(100))
    data = db.Column(db.Date, nullable=False)
    ore = db.Column(db.Float, nullable=False)
    cfu = db.Column(db.Float)
    descrizione_attivita = db.Column(db.Text)

    # Relazioni
    scuola = db.relationship('ScuoleAccreditate', backref='tirocini_diretti', lazy=True)

class RegistroPresenzeTirocinioIndiretto(db.Model):
    __tablename__ = 'RegistroPresenzeTirocinioIndiretto'
    id_tirocinio_indiretto = db.Column(db.Integer, primary_key=True)
    id_studente = db.Column(db.Integer, db.ForeignKey('Studenti.id_studente'), nullable=False)
    id_tutor_coordinatore = db.Column(db.Integer, db.ForeignKey('TutorCoordinatori.id_tutor_coordinatore'))
    data = db.Column(db.Date, nullable=False)
    ore = db.Column(db.Float, nullable=False)
    cfu = db.Column(db.Float)
    descrizione_attivita = db.Column(db.Text)

    # La relazione con il tutor coordinatore è già definita nel modello TutorCoordinatori
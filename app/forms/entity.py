from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TimeField, FloatField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, Optional

class InsegnanteForm(FlaskForm):
    nome = StringField('Nome', [DataRequired()])
    cognome = StringField('Cognome', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email()])
    telefono = StringField('Telefono', [Optional()])
    dipartimento = SelectField('Dipartimento', coerce=int)
    ssd = SelectField('SSD', coerce=int)

class ScuolaForm(FlaskForm):
    nome_scuola = StringField('Nome Scuola', [DataRequired()])
    indirizzo = StringField('Indirizzo')
    referente = StringField('Referente')
    email_referente = StringField('Email Referente', [Optional(), Email()])

class LezioneForm(FlaskForm):
    nome_lezione = StringField('Nome Lezione', [DataRequired()])
    data = DateField('Data', [DataRequired()])
    orario_inizio = TimeField('Orario Inizio', [DataRequired()])
    orario_fine = TimeField('Orario Fine', [DataRequired()])
    insegnante = SelectField('Insegnante', coerce=int)
    classi_concorso = SelectField('Classi di Concorso', coerce=int)
    dipartimenti = SelectField('Dipartimenti', coerce=int)
    percorsi = SelectField('Percorsi', coerce=int)

class PresenzaForm(FlaskForm):
    lezione = SelectField('Lezione', coerce=int, validators=[DataRequired()])
    studente = SelectField('Studente', coerce=int, validators=[DataRequired()])
    presente = SelectField('Presente', choices=[(True, 'Sì'), (False, 'No')])
    ore = FloatField('Ore')
    note = TextAreaField('Note') 
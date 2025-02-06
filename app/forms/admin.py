from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, validators
from config.roles import ROLE_ADMIN, ROLE_SEGRETERIA, ROLE_PROFESSORE, ROLE_STUDENTE, ROLE_TUTOR_COORDINATORE, ROLE_TUTOR_COLLABORATORE

class UserForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password')  # Optional per edit
    nome = StringField('Nome', [validators.DataRequired()])
    cognome = StringField('Cognome', [validators.DataRequired()])
    ruolo = SelectField('Ruolo', [validators.DataRequired()], choices=[
        (ROLE_ADMIN, 'Amministratore'),
        (ROLE_SEGRETERIA, 'Segreteria'),
        (ROLE_PROFESSORE, 'Professore'),
        (ROLE_STUDENTE, 'Studente'),
        (ROLE_TUTOR_COORDINATORE, 'Tutor Coordinatore'),
        (ROLE_TUTOR_COLLABORATORE, 'Tutor Collaboratore')
    ])
    is_active = BooleanField('Attivo') 
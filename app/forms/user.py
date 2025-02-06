from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from config.roles import (
    ROLE_ADMIN, ROLE_SEGRETERIA, ROLE_STUDENTE, ROLE_PROFESSORE,
    ROLE_TUTOR_COORDINATORE, ROLE_TUTOR_COLLABORATORE
)

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    ruolo = SelectField('Ruolo', choices=[
        (ROLE_ADMIN, 'Amministratore'),
        (ROLE_SEGRETERIA, 'Segreteria'),
        (ROLE_STUDENTE, 'Studente'),
        (ROLE_PROFESSORE, 'Professore'),
        (ROLE_TUTOR_COORDINATORE, 'Tutor Coordinatore'),
        (ROLE_TUTOR_COLLABORATORE, 'Tutor Collaboratore')
    ], validators=[DataRequired()])
    is_active = BooleanField('Attivo')
    submit = SubmitField('Salva') 
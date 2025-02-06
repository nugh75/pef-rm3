from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Accedi')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Password Attuale', validators=[DataRequired()])
    new_password = PasswordField('Nuova Password', validators=[
        DataRequired(),
        Length(min=6, message='La password deve essere di almeno 6 caratteri')
    ])
    confirm_password = PasswordField('Conferma Nuova Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Le password devono coincidere')
    ])
    submit = SubmitField('Cambia Password')
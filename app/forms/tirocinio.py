from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

class TirocinioDirettoForm(FlaskForm):
    id_studente = SelectField('Studente', coerce=int, validators=[DataRequired()])
    id_scuola = SelectField('Scuola', coerce=int, validators=[DataRequired()])
    tutor_esterno = StringField('Tutor Esterno', validators=[DataRequired(), Length(min=3)])
    data = DateField('Data', validators=[DataRequired()])
    ore = FloatField('Ore', validators=[DataRequired()])
    descrizione_attivita = TextAreaField('Descrizione Attività', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Salva')

class TirocinioIndirettoForm(FlaskForm):
    id_studente = SelectField('Studente', coerce=int, validators=[DataRequired()])
    id_tutor_coordinatore = SelectField('Tutor Coordinatore', coerce=int, validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    ore = FloatField('Ore', validators=[DataRequired()])
    descrizione_attivita = TextAreaField('Descrizione Attività', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Salva')
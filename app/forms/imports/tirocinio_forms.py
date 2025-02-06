from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class ImportTirocinioDirettoForm(FlaskForm):
    file = FileField('File Excel', validators=[FileRequired()])
    submit = SubmitField('Importa')

class ImportTirocinioIndirettoForm(FlaskForm):
    file = FileField('File Excel', validators=[FileRequired()])
    submit = SubmitField('Importa')

class ImportLezioniForm(FlaskForm):
    file = FileField('File Excel', validators=[FileRequired()])
    submit = SubmitField('Importa') 
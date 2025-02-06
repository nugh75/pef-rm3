from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ImportLezioniForm(FlaskForm):
    file = FileField('File Excel', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Solo file Excel (.xlsx, .xls)')
    ])

class ImportTirocinioIndirettoForm(FlaskForm):
    file = FileField('File Excel', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Solo file Excel (.xlsx, .xls)')
    ])

class ImportTirocinioDirettoForm(FlaskForm):
    file = FileField('File Excel', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Solo file Excel (.xlsx, .xls)')
    ]) 
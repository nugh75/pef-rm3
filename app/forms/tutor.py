from flask_wtf import FlaskForm
from wtforms import SubmitField

class DeleteTutorCollaboratoreForm(FlaskForm):
    submit = SubmitField('Elimina')
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Upload WAV File', 
                    validators=[
                        FileRequired(),
                        FileAllowed(['wav'], 'WAV files only!')
                    ])
    submit = SubmitField('Analyze')

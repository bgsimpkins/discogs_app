from wtforms import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SaveToken(Form):
    name = StringField('Current token:', validators=[DataRequired()])
    submit = SubmitField('Submit')
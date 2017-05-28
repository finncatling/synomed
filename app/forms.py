from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
	code_data = TextAreaField('code_data', validators=[DataRequired()])
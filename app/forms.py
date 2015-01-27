from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditEmployee(Form):
	fName = StringField('fName', validators= [DataRequired()])
	lName = StringField('lName', validators= [DataRequired()])
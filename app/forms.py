from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SkillSearchForm(Form):
	skillname1 = StringField('skillname1', validators= [DataRequired()])
	skillname2 = StringField('skillname2', validators= [DataRequired()])

class SkillSearchFormGeneral(Form):
	skillname1 = StringField('skillname1', validators= [DataRequired()])
	skillname2 = StringField('skillname2')

class SkillSearchFormOne(Form):
	skillname = StringField('skillname', validators= [DataRequired()])

class EditEmployee(Form):
	fName = StringField('fName', validators= [DataRequired()])
	lName = StringField('lName', validators= [DataRequired()])


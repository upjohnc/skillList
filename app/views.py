from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import Employees, Skills, skillEmpl
from .forms import LoginForm, EditEmployee

@app.route('/')
@app.route('/index')
def index():
	employees = Employees.query.all()
	skills = Skills.query.all()
	se = skillEmpl.query.all()
	combined = []

	skillsDict = {}
	for i in skills:
		skillsDict[i.id] = {'skillName' : i.skillName}

	emplDict = {}
	for i in employees:
		emplDict[i.id] = {'fName' : i.fName, 'lName' : i.lName}

	for i in se:
		combined.append({'f': emplDict[i.emplID]['fName'], 'l' :emplDict[i.emplID]['lName'], 's': skillsDict[i.skillID]['skillName']})

	return render_template('index.html',
                           title='Home',
                           se = combined)



@app.route('/edit', methods=['GET', 'POST'])
# @login_required
def editEmpl():
	Empl = Employees.query.get(1)
	form = EditEmployee()
	if form.validate_on_submit():
		Empl.fName = form.fName.data
		Empl.lName = form.lName.data
		db.session.add(Empl)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('editEmpl'))
	else:
		form.fName.data = Empl.fName
		form.lName.data = Empl.lName
	return render_template('editEmpl.html', form=form)

# suppressing login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#               (form.openid.data, str(form.remember_me.data)))
#         return redirect('/index')
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])
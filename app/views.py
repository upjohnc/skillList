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
		emplDict[i.id] = {'eid' : i.id, 'fName' : i.fName, 'lName' : i.lName}

	for i in se:
		combined.append({'eid': emplDict[i.emplID]['eid'], 'f': emplDict[i.emplID]['fName'], 'l' :emplDict[i.emplID]['lName'], 's': skillsDict[i.skillID]['skillName']})

	return render_template('index.html',
                           title='Home',
                           se = combined)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
def editEmpl(id):
	Empl = Employees.query.get(id)
	form = EditEmployee()
	if form.validate_on_submit():
		Empl.fName = form.fName.data
		Empl.lName = form.lName.data
		db.session.add(Empl)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('index'))
	else:
		form.fName.data = Empl.fName
		form.lName.data = Empl.lName
		# return redirect(url_for('index'))
	return render_template('editEmpl.html', form=form)
# EmSkillList = [(i.id, i.skillID) for i in EmSkill]
#
# AllSkills = models.Skills.query.all()
# SkillDict = {}
# for i in AllSkills:
# 	for x in EmSkillList:
# 		print(x)
# 		if i.id == x[1]:
# 			print(x[0])

@app.route('/editEskill/<int:eid>', methods = ['GET', 'POST'])
def EmplSkill(eid):
	Empl = Employees.query.get(eid)
	AllSkills = Skills.query.all()
	EmSkill = skillEmpl.query.filter_by(emplID=eid).all()
	EmSkillList = [(i.id, i.skillID) for i in EmSkill]
	SkillDict = {}
	for i in AllSkills:
		SkillDict[i.id] = {'Esid' : str(i.id) + '_' + str(eid), 'sid' : i.id, 'name' : i.skillName, 'trained' : 0}
		for x in EmSkillList:
			if i.id == x[1]:
				SkillDict[i.id] = {'Esid' : x[0], 'sid' : i.id, 'name' : i.skillName, 'trained' : 1}
	return render_template('EmplSkills.html', e = Empl, As = AllSkills, Es = SkillDict)

@app.route('/RemoveSkill/<int:id>', methods=['GET', 'POST'])
def RemoveSkill(id):
	se = skillEmpl.query.get(id)
	db.session.delete(se)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/AddSkill/<string:id>', methods=['GET', 'POST'])
def AddSkill(id):

	se = skillEmpl(skillID = int(id.split('_')[0]), emplID = int(id.split('_')[1]))
	db.session.add(se)
	db.session.commit()
	return redirect(url_for('index'))

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
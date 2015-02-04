from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import Employees, Skills, skillEmpl
from .forms import LoginForm, EditEmployee, SkillSearchForm

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
	return render_template('editEmpl.html', form=form)

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

@app.route('/skill/<string:tlist>')
def showskill(tlist):
	tasklist = {}
	# parse the search field by +
	tempList = tlist.split('+')
	# create dict from the fields parsing the values on _
	for i in tempList:
		tasklist[i.split('_')[0]] = i.split('_')[1]
	nameS = ['Skill ' + i for i in tasklist.values()]
	skills = Skills.query.filter(Skills.skillName.in_(nameS)).all()
	skillList = [i.id for i in skills]
	se = skillEmpl.query.filter(skillEmpl.skillID.in_(skillList)).all()
	resultDict = {}
	emplTestDict = {}
	for count, i in enumerate(se):
		e = Employees.query.get(i.emplID)
		s = Skills.query.get(i.skillID)
		tempEid = str(i.emplID)
		tempSid = str(i.skillID)
		if tempEid in emplTestDict.keys():
			print('hell')
			keyterm = tempEid + tempSid
			print(keyterm)
			resultDict[keyterm] = {'emplF': e.fName, 'emplL': e.lName, 'sName' : s.skillName}
			keyterm = tempEid + emplTestDict[tempEid]
			resultDict[keyterm] = {'eid' : i.emplID, 'emplF': e.fName, 'emplL': e.lName, 'sName' : emplTestDict[tempEid]}
		else:
			emplTestDict[tempEid] = s.skillName
	return render_template('SkillResults.html', tDict = resultDict)

@app.route('/SkillSearchForm', methods=['GET', 'POST'])
def doSkillSearch():
	form = SkillSearchForm()
	if form.validate_on_submit():
		# deliver search forms as seperated by + for parsing
		skilllist = 'skill1_%s+skill2_%s' % (form.skillname1.data, form.skillname2.data)
		return redirect(url_for('showskill', tlist=skilllist))
	else:
		flash('Need both fields entered.')
	return render_template('DoSearch.html', form=form)
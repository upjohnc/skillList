from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import Employees, Skills, skillEmpl
from .forms import LoginForm, EditEmployee, SkillSearchForm, SkillSearchFormOne, SkillSearchFormGeneral, EditSkill
from operator import itemgetter, attrgetter

@app.route('/')
@app.route('/index')
def index():
	employees = Employees.query.all()
	skills = Skills.query.all()
	se = skillEmpl.query.all()
	combined = {}

	skillsDict = {}
	for i in skills:
		skillsDict[i.id] = {'skillName' : i.skillName}

	emplDict = {}
	for i in employees:
		emplDict[i.id] = {'eid' : i.id, 'fname' : i.fName, 'lname' : i.lName, 'skills' : ['']}

	combined = emplDict
	for i in se:
		tempEid = emplDict[i.emplID]['eid']
		# if tempEid not in combined.keys():
		# 	combined[tempEid] = {'eid' : tempEid, 'fname': emplDict[i.emplID]['fname'], 'lname' :emplDict[i.emplID]['lname'], 'skills': [skillsDict[i.skillID]['skillName']]}
		# else:
		combined[tempEid]['skills'].append(skillsDict[i.skillID]['skillName'])

	for key, value in combined.items():
		combined[key]['skills'] = sorted(value['skills'])
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

@app.route('/addempl', methods=['GET', 'POST'])
# @login_required
def addEmpl():
	form = EditEmployee()
	if form.validate_on_submit():
		e = Employees(fName = form.fName.data, lName = form.lName.data)
		db.session.add(e)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('index'))
	else:
		form.fName.data = ''
		form.lName.data = ''
	return render_template('editEmpl.html', form=form)

@app.route('/addskill', methods=['GET', 'POST'])
# @login_required
def addSkill():
	form = EditSkill()
	if form.validate_on_submit():
		skillData = form.sName.data.split(' ')
		# add Skill to the name
		if len(skillData) > 1:
			skillData = 'Skill ' + skillData[1]
		else:
			skillData = 'Skill ' + skillData[0]

		s = Skills(skillName = skillData)
		db.session.add(s)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('index'))
	else:
		form.sName.data = ''
	return render_template('editSkill.html', form=form)

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

@app.route('/skillmultiple/<string:tlist>')
def showskillmultiple(tlist):
	tasklist = {}
	# parse the search field by +
	tempList = tlist.split('+')
	# create dict from the fields parsing the values on _
	for i in tempList:
		tasklist[i.split('_')[0]] = i.split('_')[1].lower().strip('skill ')
	nameS = ['Skill ' + i for i in tasklist.values()]
	nameS = sorted(nameS)

	resultDict = {}
	for i in nameS:
		resultDict[i] = {'skill' : i, 'empl' : []}
	skills = Skills.query.filter(Skills.skillName.in_(nameS)).all()
	skillList = [i.id for i in skills]
	se = skillEmpl.query.filter(skillEmpl.skillID.in_(skillList)).all()
	testDict = {}
	emplTestDict = {}
	for count, i in enumerate(se):
		e = Employees.query.get(i.emplID)
		s = Skills.query.get(i.skillID)
		tempEid = str(i.emplID)
		tempSid = str(i.skillID)
		if tempEid in emplTestDict.keys():
			keyterm = tempEid + tempSid
			testDict[keyterm] = {'emplF': e.fName, 'emplL': e.lName, 'sName' : s.skillName}
			keyterm = tempEid + emplTestDict[tempEid]
			testDict[keyterm] = {'eid' : i.emplID, 'emplF': e.fName, 'emplL': e.lName, 'sName' : emplTestDict[tempEid]}
		else:
			emplTestDict[tempEid] = s.skillName

	# redo result dict
	for key, values in testDict.items():
		resultDict[values['sName']]['empl'].append(values['emplF'] + ' ' + values['emplF'])
	# return render_template('EmplResults.html', tDict = testDict, sortedkeys = nameS)
	return render_template('SkillResults.html', tDict = resultDict, sortedkeys = nameS)

@app.route('/SkillSearchForm', methods=['GET', 'POST'])
def doSkillSearchMulti():
	form = SkillSearchForm()
	if form.validate_on_submit():
		# deliver search forms as seperated by + for parsing
		skilllist = 'skill1_%s+skill2_%s' % (form.skillname1.data, form.skillname2.data)
		return redirect(url_for('showskillmultiple', tlist=skilllist))
	else:
		flash('Need both fields entered.')

	return render_template('SearchMultiple.html', form=form)

@app.route('/skillone/<string:tlist>')
def showskillone(tlist):
	tlist = tlist.lower().strip('skill ')
	nameS = ['Skill ' + tlist]
	resultDict = {}
	for i in nameS:
		resultDict[i] = {'skill' : i, 'empl' : []}
	skills = Skills.query.filter(Skills.skillName.in_(nameS)).all()
	skillList = [i.id for i in skills]
	se = skillEmpl.query.filter(skillEmpl.skillID.in_(skillList)).all()
	elist = [i.emplID for i in se]
	testDict = {}
	for count, i in enumerate(se):
		e = Employees.query.get(i.emplID)
		s = Skills.query.get(i.skillID)
		tempEid = str(i.emplID)
		testDict[tempEid] = {'eid' : i.emplID, 'emplF': e.fName, 'emplL': e.lName, 'sName' : s.skillName}
	seEmployees = skillEmpl.query.filter(skillEmpl.emplID.in_(elist)).filter(~skillEmpl.skillID.in_(skillList)).all()
	for j in seEmployees:
		tempEid = str(j.emplID)
		if tempEid in testDict.keys():
			del testDict[tempEid]
	# redo result dict
	for key, values in testDict.items():
		resultDict[values['sName']]['empl'].append(values['emplF'] + ' ' + values['emplF'])
	# return render_template('EmplResults.html', tDict = testDict, sortedkeys = nameS)
	return render_template('SkillResults.html', tDict = resultDict, sortedkeys = nameS)

@app.route('/SkillSearchFormOne', methods=['GET', 'POST'])
def doSkillSearchOne():
	form = SkillSearchFormOne()
	if form.validate_on_submit():
		return redirect(url_for('showskillone', tlist=form.skillname.data))
	else:
		flash('Will search for employees with only this skill.')
	return render_template('SearchOne.html', form=form)

@app.route('/skillgeneral/<string:tlist>')
def showskillgeneral(tlist):
	tasklist = {}
	# parse the search field by +
	tempList = tlist.split('+')
	# create dict from the fields parsing the values on _
	for i in tempList:
		tasklist[i.split('_')[0]] = i.split('_')[1].lower().strip('skill ')
	nameS = ['Skill ' + i for i in tasklist.values() if i]
	nameS = sorted(nameS)
	resultDict = {}
	for i in nameS:
		resultDict[i] = {'skill' : i, 'empl' : []}

	skills = Skills.query.filter(Skills.skillName.in_(nameS)).all()
	skillList = [i.id for i in skills]
	se = skillEmpl.query.filter(skillEmpl.skillID.in_(skillList)).all()

	for count, i in enumerate(se):
		e = Employees.query.get(i.emplID)
		s = Skills.query.get(i.skillID)
		resultDict[s.skillName]['empl'].append(e.fName + ' ' + e.lName)
	return render_template('SkillResults.html', tDict = resultDict, sortedkeys = nameS)

@app.route('/SkillSearchFormGeneral', methods=['GET', 'POST'])
def doSkillSearchGeneral():
	form = SkillSearchFormGeneral()
	if form.validate_on_submit():
		# deliver search forms as seperated by + for parsing
		skilllist = 'skill1_%s+skill2_%s' % (form.skillname1.data, form.skillname2.data)
		return redirect(url_for('showskillgeneral', tlist=skilllist))
	else:
		flash('Need both fields entered.')
	return render_template('SearchGeneral.html', form=form)
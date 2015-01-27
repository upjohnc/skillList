from app import db

class Employees(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	fName = db.Column(db.String(64), index = True)
	lName = db.Column(db.String(64), index = True)

	def __repr__(self):
		return '<Employee %r, %r>' % (self.lName, self.fName)

class Skills(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	skillName = db.Column(db.String(140))

	def __repr__(self):
		return '<Skill %r>' % (self.skillName)

# section - Followers in Miguel's blog
# skillEmpl = db.Table('skillEmpl',
#                      db.Column('skillID', db.Integer, db.ForeignKey('skills.id')),
#                      db.Column('emplID', db.Integer, db.ForeignKey('employees.id'))
# 					)

class skillEmpl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	skillID = db.Column(db.Integer, db.ForeignKey('skills.id'))
	emplID = db.Column(db.Integer, db.ForeignKey('employees.id'))

	def __repr__(self):
		return '<Empl ID %r, Skill ID %r>' % (self.emplID, self.skillID)
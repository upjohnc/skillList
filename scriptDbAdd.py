from app import db, models

e = models.Employees(fName = 'Chad', lName = 'Upjohn')
db.session.add(e)
e = models.Employees(fName = 'Cheryl', lName = 'Aber')
db.session.add(e)
db.session.commit()

s = models.Skills(skillName = 'Skill 111')
db.session.add(s)
s = models.Skills(skillName = 'Skill 222')
db.session.add(s)
db.session.commit()


print(models.Employees.query.all())

e = models.Employees.query.all()
s = models.Skills.query.all()

se = models.skillEmpl(emplID = e[0].id, skillID = s[0].id)
db.session.add(se)
se = models.skillEmpl(emplID = e[0].id, skillID = s[1].id)
db.session.add(se)
se = models.skillEmpl(emplID = e[1].id, skillID = s[1].id)
db.session.add(se)
db.session.commit()

se = models.skillEmpl.query.get(1)
db.session.delete(se)
db.session.commit()

print(models.skillEmpl.query.all())

# skillEmpl(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	skillID = db.Column(db.Integer, db.ForeignKey('Skills.id'))
# 	emplID = db.Column(db.Integer, db.ForeignKey('Employees.id'))

from app import db, models

import pandas as pd

df = pd.read_csv('cariList.csv',  delimiter = '\t')

df['first'] = df['Name'].map(lambda x: x.split(', ')[1])
df['last'] = df['Name'].map(lambda x: x.split(', ')[0])

for i in df.index:
	e = models.Employees(fName = df.ix[i, 'first'], lName = df.ix[i, 'last'])
	db.session.add(e)

db.session.commit()

# e = models.Employees(fName = 'Chad', lName = 'Upjohn')
# db.session.add(e)
# e = models.Employees(fName = 'Cheryl', lName = 'Aber')
# db.session.add(e)
# db.session.commit()

s = models.Skills(skillName = 'Skill 111')
db.session.add(s)
s = models.Skills(skillName = 'Skill 222')
db.session.add(s)
s = models.Skills(skillName = 'Skill 333')
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
se = models.skillEmpl(emplID = e[1].id, skillID = s[2].id)
db.session.add(se)
db.session.commit()

# se = models.skillEmpl.query.get(1)
# db.session.delete(se)
# db.session.commit()

print(models.skillEmpl.query.all())

# skillEmpl(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	skillID = db.Column(db.Integer, db.ForeignKey('Skills.id'))
# 	emplID = db.Column(db.Integer, db.ForeignKey('Employees.id'))

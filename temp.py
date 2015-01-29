from app import models, db

list = ('111', '222')
nameS = ['Skill ' + x for x in list]
skills = models.Skills.query.filter(models.Skills.skillName.in_(nameS)).all()
skillList = [i.id for i in skills]
se = models.skillEmpl.query.filter(models.skillEmpl.skillID.in_(skillList)).all()
resultDict = {}
for i in se:
	print(i.emplID)
	# print(se[i].emplID)
# skills = models.Skills.query.all()
# se = models.skillEmpl.query.all()
# combined = []
#
# skillsDict = {}
# for i in skills:
# 	skillsDict[i.id] = {'skillName' : i.skillName}
#
# emplDict = {}
# for i in employees:
# 	emplDict[i.id] = {'fName' : i.fName, 'lName' : i.lName}
#
# # print(skills.id)
# # for x in skills:
# # 	print(x.id)
# # combined ={{ 'fName' : '1', 'other' : '2' }, {'fName': '3', 'other' : '4'}}# }
# for i in se:
# 	combined.append({'f': emplDict[i.emplID]['fName'], 's': skillsDict[i.skillID]['skillName']})
# 	# combined.append(temp)
#
# print(combined)
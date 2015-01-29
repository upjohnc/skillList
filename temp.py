from app import models, db

EmSkill = models.skillEmpl.query.filter_by(emplID=2).all()
EmSkillList = [(i.id, i.skillID) for i in EmSkill]

AllSkills = models.Skills.query.all()
SkillDict = {}
for i in AllSkills:
	for x in EmSkillList:
		print(x)
		if i.id == x[1]:
			print(x[0])

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
from app import db, models

import pandas as pd

df = pd.read_csv('cariList.csv',  delimiter = '\t')

df['first'] = df['Name'].map(lambda x: x.split(', ')[1])
df['last'] = df['Name'].map(lambda x: x.split(', ')[0])

for i in df.index:
	e = models.Employees(fName = df.ix[i, 'first'], lName = df.ix[i, 'last'])
	db.session.add(e)

db.session.commit()

temp = pd.read_csv('Agent_Daily_Prod.csv')
temp = temp[['Split/Skill', 'Login_ID']]

def split(x):
    jj = x.split(' ')
    if len(jj) > 1:
        return jj[1].capitalize()
    else:
        return ''
temp['fname'] = temp['Login_ID'].map(split)
temp['lname'] = temp['Login_ID'].map(lambda x: x.split(' ')[0].capitalize())

import string
def split(x):
    jj = x.strip().split(' ')
    if len(jj) > 1:
        return jj[1]
    else:
        return jj[0].strip(string.ascii_letters)
temp['Skill'] = temp['Split/Skill'].map(split)

def split(x):
    jj = x.strip().split(' ')
    if len(jj) > 1:
        return jj[0]
    else:
        return ''
temp['tempFname'] = temp['Split/Skill'].map(split)

for z in temp.index:
    if temp.ix[z, 'fname'] is '':
        temp.ix[z, 'fname'] = temp.ix[z, 'tempFname']

temp['Skill'] = 'Skill ' + temp['Skill']
temp['fname'] = temp['fname'].map(lambda x: x.strip(string.digits))

temp2 = temp[['fname', 'lname', 'Skill']]

skill_list = temp2['Skill'].unique()

for i in skill_list:
    s = models.Skills(skillName = i)
    db.session.add(s)

db.session.commit()


print(models.Employees.query.all())

temp3 = temp[['fname', 'lname', 'Skill']]

e = models.Employees.query.all()
s = models.Skills.query.all()

e_dict = {}
for ie in e:
	e_dict[ie.id] = {'fname' : ie.fName, 'lname' : ie.lName}

s_dict = {}
for js in s:
	s_dict[js.id] = {'skillname' : js.skillName}

dfE = pd.DataFrame(e_dict).T.reset_index(drop=False)
dfS = pd.DataFrame(s_dict).T.reset_index(drop=False)

temp3 = temp3.merge(dfS, how = 'left', left_on = 'Skill', right_on = 'skillname')
temp3 = temp3.merge(dfE, how = 'left', left_on = ['fname', 'lname'], right_on = ['fname', 'lname'])
temp3.columns = ['fname', 'lname', 'skill', 'sid', 'skillname', 'eid']

temp4 = temp3.dropna(subset = ['eid'], axis = 0)

temp4.drop_duplicates(inplace=True)

for i in temp4.index:
    se = models.skillEmpl(emplID = int(temp4.ix[i, 'eid']), skillID = int(temp4.ix[i, 'sid']))
    db.session.add(se)

db.session.commit()

print(models.skillEmpl.query.all())
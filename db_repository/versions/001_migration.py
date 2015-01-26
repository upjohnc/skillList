from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
skill_empl = Table('skill_empl', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('skillID', Integer),
    Column('emplID', Integer),
)

skills = Table('skills', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('skillName', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['skill_empl'].create()
    post_meta.tables['skills'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['skill_empl'].drop()
    post_meta.tables['skills'].drop()

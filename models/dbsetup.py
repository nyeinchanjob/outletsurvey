from datetime import datetime
from gluon.contrib.appconfig import AppConfig
import os
myconf = AppConfig(reload=True)




## outlet
db.define_table("outlet",
    Field("name", "string", requires=IS_NOT_EMPTY()),
    Field('is_active', 'boolean', default=True, label="Active"),
	Field('created_on', 'datetime', default=request.now,
			readable=True, writable=False),
	Field('created_by', 'reference auth_user', default=auth.user_id,
			readable=True, writable=False),
	Field('modified_on', 'datetime', update=request.now,
			readable=True, writable=False),
	Field('modified_by', 'reference auth_user', update=auth.user_id,
			readable=True, writable=False),
	format='%(name)s'
)


## question
db.define_table("question",
    Field("name", "string", requires=IS_NOT_EMPTY()),
    Field('is_active', 'boolean', default=True, label="Active"),
	Field('created_on', 'datetime', default=request.now,
			readable=True, writable=False),
	Field('created_by', 'reference auth_user', default=auth.user_id,
			readable=True, writable=False),
	Field('modified_on', 'datetime', update=request.now,
			readable=True, writable=False),
	Field('modified_by', 'reference auth_user', update=auth.user_id,
			readable=True, writable=False),
	format='%(name)s'
)

db.define_table("survey",
    Field("area", "string", requires=IS_NOT_EMPTY(), label="Area"),
    Field("city_mm", "string", label="City(MM)"),
    Field("city_en", "string", label="City(EN)"),
    Field("township_mm", "string", label="Township(MM)"),
    Field("township_en", "string", label="Township(EN)"),
    Field("ward_mm", "string", label="Ward(MM)"),
    Field("ward_en", "string", label="Ward(EN)"),
    Field("outlet_type", "reference outlet", label="Outlet Type"),
    Field("outlet_mm", "string", label="Outlet(MM)", requires=IS_NOT_EMPTY()),
    Field("outlet_en", "string", label="Outlet(EN)", requires=IS_NOT_EMPTY()),
    Field("owner_mm", "string", label="Owner(MM)", requires=IS_NOT_EMPTY()),
    Field("owner_en", "string", label="Owner(EN)", requires=IS_NOT_EMPTY()),
    Field("phone1", "string", label="Phone1"),
    Field("phone2", "string", label="Phone2"),
    Field("phone3", "string", label="Phone3"),
    Field("image1", "upload", uploadfolder=os.path.join('uploads/image1')),
    Field("image2", "upload", uploadfolder=os.path.join('uploads/image2')),
    Field("image3", "upload", uploadfolder=os.path.join('uploads/image3')),
    Field("latitude", "string", label="Latitude", requires=IS_NOT_EMPTY()),
    Field("longitude", "string", label="Longitude", requires=IS_NOT_EMPTY()),
    Field('is_active', 'boolean', default=True, label="Active"),
	Field('created_on', 'datetime', default=request.now,
			readable=True, writable=False),
	Field('created_by', 'reference auth_user', default=auth.user_id,
			readable=True, writable=False),
	Field('modified_on', 'datetime', update=request.now,
			readable=True, writable=False),
	Field('modified_by', 'reference auth_user', update=auth.user_id,
			readable=True, writable=False),
	format=lambda r: '%s [%s]' % (r.outlet_en, r.city_en)
)

db.survey.outlet_type.requires=IS_IN_DB(db(db.outlet.is_active==True), db.outlet.id, '%(name)s')

db.define_table("survey_detail",
    Field("survey_id", "reference survey", readable=False),
    Field("question_id", "reference question", label="Question", requires=IS_NOT_EMPTY()),
    Field("answer", "integer", requires=IS_NOT_EMPTY(), label="Answer")
)

db.survey_detail.question_id.requires=IS_IN_DB(db(db.question.is_active==True), db.question.id, '%(name)s')

## default user root
if db(db.auth_user).count()<1:
    db.auth_group.bulk_insert([
    	dict(role='Admin', description='System user'),
		dict(role='Manager', description='Manager'),
		dict(role='User', description='User')
	])
    db.auth_user.bulk_insert([
		dict(
			first_name='System',
			last_name='Admin',
			email='root@coca-cola.com.mm',
			password=db.auth_user.password.validate('C0ke@12345')[0]
		),
		dict(
			first_name='Nyein',
			last_name='Chan',
			email='nyeinchan@coca-cola.com.mm',
			password=db.auth_user.password.validate('Basn4@C01')[0]
		)
	])
    auth.add_membership(user_id=1, group_id=1)
    auth.add_membership(user_id=2, group_id=1)

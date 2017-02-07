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
    Field("area", "string", label="Area"),
    Field("outlet_id", "string", label="Area"),
    Field("city_mm", "string", label="City(MM)"),
    Field("city_en", "string", label="City(EN)"),
    Field("township_mm", "string", label="Township(MM)"),
    Field("township_en", "string", label="Township(EN)"),
    Field("ward_mm", "string", label="Ward(MM)"),
    Field("ward_en", "string", label="Ward(EN)"),
    Field("street_mm", "string", label="No And Street (MM)"),
    Field("street_en", "string", label="No And Street (EN)"),
    Field("outlet_type", "reference outlet", label="Outlet Type"),
    Field("outlet_mm", "string", label="Outlet(MM)", requires=IS_NOT_EMPTY()),
    Field("outlet_en", "string", label="Outlet(EN)", requires=IS_NOT_EMPTY()),
    Field("owner_mm", "string", label="Owner(MM)", requires=IS_NOT_EMPTY()),
    Field("owner_en", "string", label="Owner(EN)", requires=IS_NOT_EMPTY()),
    Field("phone1", "string", label="Phone1"),
    Field("phone2", "string", label="Phone2"),
    Field("phone3", "string", label="Phone3"),
    Field("cooler_model", "string", label="Cooler Model"),
    Field("cooler_sn", "string", label="Cooler S/N"),
    Field("image1", "upload", uploadfolder=os.path.join('uploads/image1')),
    Field("image2", "upload", uploadfolder=os.path.join('uploads/image2')),
    Field("image3", "upload", uploadfolder=os.path.join('uploads/image3')),
    Field("latitude", "double", label="Latitude", requires=IS_NOT_EMPTY()),
    Field("longitude", "double", label="Longitude", requires=IS_NOT_EMPTY()),
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


def questionlist(row):
    questions = db((db.survey_detail.survey_id == row.survey.id) &
                 (db.survey_detail.question_id == db.question.id)).select(
                    db.survey_detail.id,
                    db.question.name,
                    db.survey_detail.answer
                 )
    _ids = [str(question.survey_detail.id) for question in questions]
    return ",".join(_ids)


max_cols = 30
if db(db.question).count()>1:
    max_cols = db(db.question).count()

_previous_id = 0
_counter = 0

def subquestionlist(row):
    global max_cols, _counter, _previous_id
    splitted = row.survey.questions.split(",")
    len_splitted = len(splitted)
    if len_splitted:
        if not splitted[-1]:
            len_splitted = 0

    if len_splitted:
        tmp_row = [ splitted[i] if len_splitted > i else None for i in range(max_cols)]
    else:
        tmp_row = [ None for i in range(max_cols)]

    # print "subquestionlist >>>", _counter, 'survey_id:', row.survey.id, 'splitted:', len_splitted

    if not _previous_id:
        _previous_id = row.survey.id
    else:
        if _previous_id != row.survey.id:
            _previous_id = row.survey.id
            _counter = 0
        else:
            _counter += 1

    if len(tmp_row) > _counter:
        value = tmp_row[_counter]
    else:
        value = -1

    row = db((db.survey_detail.id == value) &
                 (db.survey_detail.question_id == db.question.id)).select(
                    db.survey_detail.id,
                    db.question.name,
                    db.survey_detail.answer
                 ).last()
    if row:
        return "%s" % (row.survey_detail.answer)
    else:
        return ""

db.survey.questions = Field.Virtual("questions", questionlist)
for row in db(db.question).select():
    _field_name = "_".join(row.name.replace("(", "").replace(")", "").replace("-", "").replace("/", "_").split(" "))
    # print _field_name
    db.survey[_field_name] = Field.Virtual(_field_name, subquestionlist)

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
            custom_password = 'Basn4@C01',
			password=db.auth_user.password.validate('Basn4@C01')[0]
		)
	])
    auth.add_membership(user_id=1, group_id=1)
    auth.add_membership(user_id=2, group_id=1)

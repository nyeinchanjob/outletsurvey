# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.serializers import json
from gluon.tools import geocode

@auth.requires_login()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


def outlet():
    grid = SQLFORM.smartgrid(
        db.outlet,
        paginate=10,
        csv=False,
        details=False,
        orderby =~db.outlet.id,
        linked_tables=False,
		editable=auth.has_membership('Admin', 'Manger')
    )
    response.moduleTitle = 'Outlet Type'
    return dict(form=grid)


def question():
    grid = SQLFORM.smartgrid(
        db.question,
        paginate=10,
        csv=False,
        details=False,
        orderby =~db.question.id,
        linked_tables=False
    )
    response.moduleTitle = 'Question Type'
    return dict(form=grid)

def location():
	form=SQLFORM.factory(Field('latitude', label='Latitude', requires=IS_NOT_EMPTY()),
			Field('longitude', label='Longitude', requires=IS_NOT_EMPTY()),
			Field('search'), _class='form-search'
	)
	#form.custom.widget.search['_class'] = 'input-long search-query'
	#form.custom.submit['_value'] = 'Search'
	#form.custom.submit['_class'] = 'btn'
	response.moduleTitle = 'Locaiton'
	return dict(form=form)

def survey():
    def redirectToDetail(form):
        survey_id = form.vars.id
        redirect(URL('surveydetail', vars=dict(survey_id=survey_id)))
    form = SQLFORM.grid(db.survey, fields=[db.survey.id, db.survey.outlet_en,
        db.survey.outlet_type, db.survey.owner_en,
        db.survey.phone1, db.survey.ward_en,
        db.survey.township_en, db.survey.city_en,
        db.survey.area],
            csv=False,
            details=False,
            paginate=20,
            orderby=~db.survey.id|db.survey.city_en,
            user_signature=False,
            oncreate=redirectToDetail,
            onupdate=redirectToDetail)
    response.moduleTitle = 'Outlet Information'
    return dict(form=form)

def surveydetail():
    survey_id = request.vars.survey_id
    if type(survey_id) == list:
        survey_id = survey_id[-1]
    db.survey_detail.survey_id.default = survey_id
    db.survey_detail.survey_id.readable = False
    form = SQLFORM(db.survey_detail)
    form.add_button("Back", URL('default', 'survey'))
    if form.process().accepted:
        redirect(URL('surveydetail', vars=dict(survey_id=survey_id)))
    response.moduleTitle = 'Question and Answer'
    return dict(form=form, survey_id=survey_id)

def surveydetaillist():
    survey_id = request.vars.survey_id
    where = (db.survey_detail.survey_id == survey_id)
    grid = SQLFORM.grid(where, create=False, editable=False, details=False, csv=False)
    return dict(grid=grid)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def about():

    response.moduleTitle = 'About'
    return dict(message=T('Welcome Outlet Survey System!'))

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    response.menu = [
    (T('HOME'), False, A('HOME',_href= URL('default','index'),_class='active'), []),
    (T('DESPRE NOI'), False, URL('default','despre_noi'), []),
    (T('PROIECTE'), False, URL('default','proiecte'), []),
    (T('CONTACT'), False, URL('default','contact'), [])
    ]
    return locals()

def despre_noi():
    response.menu = [
    (T('HOME'), False, URL('default','index'), []),
    (T('DESPRE NOI'), False, A('DESPRE_NOI',_href= URL('default','despre_noi'),_class='active'), []),
    (T('PROIECTE'), False, URL('default','proiecte'), []),
    (T('CONTACT'), False, URL('default','contact'), [])
    ]
    return locals()

def proiecte():
    response.menu = [
    (T('HOME'), False, URL('default','index'), []),
    (T('DESPRE NOI'), False, URL('default','despre_noi'), []),
    (T('PROIECTE'), False, A('PROIECTE',_href= URL('default','proicte'),_class='active'), []),
    (T('CONTACT'), False, URL('default','contact'), [])
    ]
    return locals()

def contact():
    response.menu = [
    (T('HOME'), False, URL('default','index'), []),
    (T('DESPRE NOI'), False, URL('default','despre_noi'), []),
    (T('PROIECTE'), False, URL('default','proiecte'), []),
    (T('CONTACT'), False, A('CONTACT',_href= URL('default','contact'),_class='active'), [])
    ]
    form = SQLFORM.factory(
        Field('name', requires=IS_NOT_EMPTY(), default='Nume'),
        Field('companie', default='Companie (optional)'),
        Field('email', requires=IS_NOT_EMPTY(), default='Adresa ta de email'),
        Field('mesaj', 'text', requires=IS_NOT_EMPTY(), default='Mesaj'),
        submit_button='Trimite')
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        session.your_name = form.vars.your_name
        session.filename = form.vars.your_image
    elif form.errors:
        response.flash = 'form has errors'
    return locals()


def user():
    return dict(form=auth())

def download():
    return response.download(request,db)


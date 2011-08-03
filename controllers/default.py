# -*- coding: utf-8 -*-

def index():
    return locals()

def despre_noi():
    return locals()

def proiecte():
    return locals()

def contact():
    form = SQLFORM.factory(
        Field('nume', requires=IS_NOT_EMPTY(), default='Nume'),
        Field('companie', default='Companie (optional)'),
        Field('email', requires=IS_EMAIL(error_message=T('adresa de email invalida!')), default='Adresa ta de email'),
        Field('mesaj', 'text', requires=IS_NOT_EMPTY(), default='Mesaj'),
        submit_button='Trimite')
    if form.accepts(request.vars, session):
        response.flash = 'multumim! mesaj trimis!'
        mail.send('rif@mailinator.com', 'Message de la %s(%s)'%(form.vars.nume, form.vars.companie), form.vars.mesaj + "\nreplay-to: " + form.vars.email)

    elif form.errors:
        response.flash = 'formularul contine erori'
    return locals()


def user():
    return dict(form=auth())

def download():
    return response.download(request,db)


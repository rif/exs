# -*- coding: utf-8 -*-

def index():
    return locals()

def despre_noi():
    return locals()

def proiecte():
    categoria = db.category(request.vars['cat']) if 'cat' in request.vars else  None
    tagul = db.tag(request.vars['tag']) if 'tag' in request.vars else  None
    
    if len(request.args): page=int(a0)
    else: page=0
    items_per_page=6
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    
    proiecte = None
    if categoria:
        proiecte = categoria.project
    if categoria and tagul:
        proiecte = db((db.project.category==categoria) & (db.project.tags.contains(tagul.id)))
    if not proiecte:
        proiecte = db(db.project)
    proiecte = proiecte.select(orderby=~db.project.year, limitby=limitby)
    
    ids = ('doi-doi', 'doi-trei', 'doi-patru', 'trei-doi', 'trei-trei', 'trei-patru')
    divs = [DIV(IMG(_src=URL('download', args=db((db.picture.project==p)&(db.picture.representative==True)).select().first().image), _alt=p.name +'picture', _title=p.year), _id=ids[i%items_per_page]) for i,p in enumerate(proiecte)]
    return dict(divs=divs, page=page,items_per_page=items_per_page)

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


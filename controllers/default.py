# -*- coding: utf-8 -*-

def index():
    proiecte = db((db.project.is_active==True) & (db.project.representative==True)).select()[:3]
    ids = ('doi-doi', 'doi-trei', 'doi-patru')
    divs = []
    for i,p in enumerate(proiecte):
        pic = db((db.picture.project==p)&(db.picture.representative==True)).select().first()
        if not pic: pic = db(db.picture.project==p).select().first() # get the first picture
        if pic:
            divs.append(DIV(A(IMG(_src=URL('download', args=pic.gray), _alt=p.name +' picture', _title=str(p.year) + ": " + p.description, _class="prj-img"), _href=URL('proiecte')), _id=ids[i]))
        else: # if project has no pictures
            divs.append(DIV(A('No picture for project %s' % p.name, _href=URL('proiecte')), _id=ids[i]))
    return locals()

def despre_noi():
    abo = db(db.about).select().first()
    return locals()

def proiecte():
    an = request.vars.year
    tagul = db.tag(request.vars.tag)
    
    if len(request.args): page=int(a0)
    else: page=0
    items_per_page=6
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    
    query = active_projects_query & project_pictures_query
    if an and an != 'None': query &= (db.project.year == an)
    if tagul: query &= db.picture.tags.contains(tagul.id)
    proiecte = db(query).select(orderby=~db.project.year, limitby=limitby, groupby=db.project.id)
    years = db(db.project).select(db.project.year, distinct=True, orderby=~db.project.year)
    
    ids = ('doi-doi', 'doi-trei', 'doi-patru', 'trei-doi', 'trei-trei', 'trei-patru')
    divs = []
    tag_id = tagul.id if tagul else -1
    for i,row in enumerate(proiecte):
        p = row.project
        pic = db((db.picture.project==p.id)&(db.picture.representative==True)).select().first()
        if not pic: pic = db(db.picture.project==p.id).select().first() # get the first thumbnail
        if pic:
            divs.append(DIV(A(IMG(_src=URL('download', args=pic.thumb), _alt=p.name +' picture', _title=str(p.year) + ": " + p.description, _class="prj-img"), _href=URL('galerie', args=p.id, vars={'tag': tag_id}),_class='galerie'), _id=ids[i%items_per_page]))
        else: # if project has no pictures
            divs.append(DIV(A('No picture for project %s' % p.name, _href=URL('galerie', args=p.id, vars={'tag': tag_id}),_class='galerie'), _id=ids[i%items_per_page]))
    return dict(divs=divs, page=page,items_per_page=items_per_page, years=years)

def contact():
    form = SQLFORM.factory(
        Field('nume', requires=IS_NOT_EMPTY(), default='Nume'),
        Field('companie', default='Companie (optional)'),
        Field('email', requires=IS_EMAIL(error_message=T('adresa de email invalida!')), default='Adresa ta de email'),
        Field('mesaj', 'text', requires=IS_NOT_EMPTY(), default='Mesaj'),
        submit_button='Trimite')
    if form.accepts(request.vars, session):
        response.flash = 'multumim! mesaj trimis!'
        abo = db(db.about).select().first()
        email_to = abo.email if abo else 'exs@mailinator.com'
        mail.send(email_to, 'Message de la %s(%s)'%(form.vars.nume, form.vars.companie), form.vars.mesaj + "\nreplay-to: " + form.vars.email)
    elif form.errors:
        response.flash = 'formularul contine erori'
    abo = db(db.about).select().first()
    return locals()

def galerie():
    tagul = db.tag(request.vars.tag)
    query = db.picture.project==a0
    if tagul: query &= db.picture.tags.contains(tagul.id)
    pics = db(query).select()
    return locals()

def panou():
    pic = db.picture(a0)
    index = int(a1)
    count = int(a2)
    counter = "%s/%s " %(a1, a2)
    return locals()

def user():
    return dict(form=auth())

def download():
    return response.download(request,db)


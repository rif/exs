# -*- coding: utf-8 -*-
import math

def index():
    #an = request.vars.year
    tagul = db.tag(request.vars.tag)

    if len(request.args): page=int(a0)
    else: page=0
    items_per_page=6
    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    query = active_projects_query & project_pictures_query
    #if an and an != 'None': query &= (db.project.year == an)
    if tagul: query &= db.picture.tags.contains(tagul.id)
    proiecte = db(query).select(orderby=~db.project.year, limitby=limitby, groupby=db.project.id)
    toate_proiectele = db(query).select(groupby=db.project.id)
    max_pages = int(math.ceil(float(len(toate_proiectele))/items_per_page)) or 1

    #if tagul:
    #    years = db(query).select(db.project.year, distinct=True, orderby=~db.project.year)
    #else:
    #    years = db(db.project).select(db.project.year, distinct=True, orderby=~db.project.year)

    ids = ('doi-doi', 'doi-trei', 'doi-patru', 'trei-doi', 'trei-trei', 'trei-patru')
    divs = []
    tag_id = tagul.id if tagul else -1
    for i,row in enumerate(proiecte):
        p = row.project
        query = db.picture.project==p.id
        if tagul:
          query &= db.picture.tags.contains(tagul.id)
        else:
          query &= db.picture.representative==True
        pic = db(query).select().first()
        if not pic: pic = db(db.picture.project==p.id).select().first() # get the first thumbnail
        if pic:
            divs.append(DIV(A(IMG(_src=URL('download', args=pic.thumb), _alt=p.name +' picture', _title=str(p.year) + ": " + p.description, _class="prj-img"), _href=URL('galerie', args=p.id, vars={'tag': tag_id}),_class='galerie'), _id=ids[i%items_per_page]))
        else: # if project has no pictures
            divs.append(DIV(A('No picture for project %s' % p.name, _href=URL('galerie', args=p.id, vars={'tag': tag_id}),_class='galerie'), _id=ids[i%items_per_page]))
    return dict(divs=divs, page=page,items_per_page=items_per_page, max_pages=max_pages)

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
    project = db.project(a0)
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

def access():
    import os, hashlib
    files = []
    dirname = ''
    project = ''
    path = os.path.join(request.folder, 'static/projects/')
    cod_valid = False
    form = SQLFORM.factory(Field('project_code'),submit_button='Trimite')
    project_code = a0
    if form.accepts(request.vars, session):        
        project_code = form.vars.project_code            
    for d in os.listdir(path):        
        if hashlib.sha1(d).hexdigest() == project_code:
            cod_valid = True
            dirname = os.path.join('projects/',d)
            project = d
            files = os.listdir(os.path.join(path, d))
            # sort by modification time in reverse order (latest first)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(path,d,x)), reverse=True)
            files = [(f, __sizeof_fmt(os.path.getsize(os.path.join(path,d,f)))) for f in files]
    return locals()

def __sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

@auth.requires_permission('read', 'about')
def access_codes():
    import os,hashlib
    path = os.path.join(request.folder, 'static/projects/')
    projects = []
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path,d)):
            code = hashlib.sha1(d).hexdigest()
            projects.append((d, code, 'http://www.exstudio.ro/init/default/access/' +  code))
    return locals()

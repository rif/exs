# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('EXStudio')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Radu Fericean'
response.meta.description = 'EXStudio website'
response.meta.keywords = 'aritecture, design, interior, exterior'
response.meta.generator = 'Web2py Enterprise Framework'



response.menu = [
    (T('HOME'), False, URL('default','index'), []),
    (T('PROIECTE'), False, URL('default','proiecte'), []),
    (T('CONTACT'), False, URL('default','contact'), [])
    ]


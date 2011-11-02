# -*- coding: utf-8 -*-

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('google:datastore')              # connect to Google BigTable
                                              # optional DAL('gae://namespace')
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []


from gluon.tools import Mail, Auth, Crud, Service, PluginManager, prettydate
mail = Mail()                                  # mailer
auth = Auth(db)                                # authentication/authorization
crud = Crud(db)                                # for CRUD helpers using auth
service = Service()                            # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()                      # for configuring plugins

mail.settings.server = 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'ustest@gmail.com'         # your email
mail.settings.login = 'ustest:greta.1'      # your credentials or None

auth.settings.hmac_key = 'sha512:e68b4107-4595-4284-9cd1-ef04a2ed3205'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

crud.settings.auth = None        # =auth to enforce authorization on crud

db.define_table('tag',
    Field('name'),
    Field('order_index', 'integer'),
    format='%(name)s'
 )

db.define_table('project',
    Field('name'),
    Field('description', 'text', represent=lambda d: MARKMIN(d)),
    Field('year', 'integer'),
    auth.signature,
    format='%(name)s'
)

db.define_table('picture',
    Field('project', db.project),
    Field('image', 'upload', required=True, notnull=True),
    Field('thumb', 'upload', required=True, notnull=True),
    Field('gray', 'upload', compute=lambda r: make_gray(r.thumb)),
    Field('title'),
    Field('description', 'text', represent=lambda d: MARKMIN(d)),
    Field('representative', 'boolean', comment='Will be display as cover for project'),
    Field('tags', 'list:reference tag'),
    auth.signature,
    format='%(title)s'
)

db.define_table('about',
    Field('email', requires=IS_EMAIL()),
    Field('description', 'text', represent=lambda d: MARKMIN(d), length=2048, comment="You can use markmin syntax, see here: http://web2py.com/examples/static/markmin.html"),
    Field('address', 'text', represent=lambda d: MARKMIN(d), comment="You can use markmin syntax, see here: http://web2py.com/examples/static/markmin.html"),
    Field('claudiu', 'upload', required=True),
    Field('tibi', 'upload', required=True),
    Field('news', 'text', represent=lambda d: MARKMIN(d), comment="You can use markmin syntax, see here: http://web2py.com/examples/static/markmin.html"),
)

def make_gray(pictureImg):
    try:
        import uuid
        from PIL import Image, ImageOps
    except: return
    size = 84, 84
    im=Image.open(request.folder + 'uploads/' + pictureImg)    
    im.thumbnail(size)
    grayName='picture.gray.%s.jpg' % (uuid.uuid4())
    im.save(request.folder + 'uploads/' + grayName, 'JPEG')
    return grayName

a0,a1,a2 = request.args(0), request.args(1), request.args(2)
active_projects_query = (db.project.is_active == True)
project_pictures_query = (db.project.id == db.picture.project)
abo = db(db.about).select().first()

plugins.instant_admin.extra_sidebar_title = "Client access"
plugins.instant_admin.extra_sidebar = [
    A('Access codes', _href=URL('default','access_codes')),
]

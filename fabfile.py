from fabric.api import sudo, prompt, run, local, cd
from fabric.decorators import runs_once, hosts, task
from fabric.colors import green

@task
def ci():
    'Commit localy using mercurial'
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('compass compile -e production --force static')
    local('hg ci -m "%s"' % comment)
    push()

@runs_once
def push():
    print(green('pushing...'))
    local('hg push')

@task
@hosts('exserver@www.exstudio.ro:22011')
def deploy():
    'triggers hg pul on the server'
    print(green('deploying...'))
    push()
    'Deploy the app to the target environment'
    with cd('web2py/applications/init/'):
        run('hg pul -uv')
    recompile()

@task
@hosts('exserver@www.exstudio.ro:22011')
def recompile():
    'recompile application'
    print(green('recompiling...'))
    with cd('web2py'):
        run('python -c "import gluon.compileapp; gluon.compileapp.compile_application(\'applications/init\')"')

@task
@hosts('exserver@www.exstudio.ro:22011')
def reload():
    'fires an apache graceful reload'
    print(green('reloading...'))
    sudo('apachectl graceful')

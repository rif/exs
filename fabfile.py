from fabric.api import sudo, prompt, run, local, cd
from fabric.decorators import runs_once, hosts, task
from fabric.colors import green

@task
def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('hg ci -m "%s"' % comment)
    push()

@runs_once
def push():
    local('hg push')

@task
@hosts('rif@avocadosoft.ro:22011')
def deploy():
    'triggers hg pul on the server'
    push()
    'Deploy the app to the target environment'
    with cd('../www-data/web2py/applications/exs/'):
        run('hg pul -uv')

@task
@hosts('rif@avocadosoft.ro:22011')
def reload():
    'fires an apache graceful reload'
    sudo('apachectl graceful')

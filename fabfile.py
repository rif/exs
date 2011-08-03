from fabric.api import hosts, prompt, sudo, run, local, cd

def ci():
    """Commit localy using mercurial"""
    comment = prompt('Commit comment: ', default='another commit from fabric')
    local('hg ci -m "%s"' % comment)
    local('hg push')

@hosts('rif@avocadosoft.ro:22011')
def deploy():
    'Deploy the app to the target environment'
    #local('hg push')
    with cd('../www-data/web2py/applications/exs/'):
        run('hg pul -uv')

@hosts('rif@avocadosoft.ro:22011')
def reload():
    'fires an apache graceful reload'
    sudo('apachectl graceful')

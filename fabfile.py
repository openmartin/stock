from fabric.api import *

env.hosts = ['ubuntu@ec2-54-254-116-230.ap-southeast-1.compute.amazonaws.com']

def test():
    local("./manage.py test my_app")

def commit():
    #local("git add -p && git commit")
    pass

def push():
    local("git push origin")

def prepare_deploy():
    #test()
    commit()
    push()
    
def remote_pull():
    run('cd djenv')
    run('source bin/activate')
    run('cd stock')
    run('git pull')

def remote_restart():
    pass

def deploy():
    prepare_deploy()
    remote_pull()
    remote_restart()
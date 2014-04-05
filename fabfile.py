from __future__ import with_statement
from fabric.api import *

env.hosts = ['ec2-54-254-116-230.ap-southeast-1.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = 'E:\\py_workspace\\zilikey.pem'
env.activate = 'source ~/djenv/bin/activate'

def test():
    local("./manage.py test my_app")

def commit():
    with settings(warn_only=True):
        local("git add -p && git commit")

def push():
    local("git push origin")

def prepare_deploy():
    #test()
    commit()
    push()
    
def remote_pull():
    with cd("djenv/stock"):
        run("git pull")

def remote_restart():
    run("kill -HUP `ps -ef | grep uwsgi | awk '($3==1){print $2}'`")
    sudo("/etc/init.d/nginx restart")

def deploy():
    prepare_deploy()
    remote_pull()
    remote_restart()
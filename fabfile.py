#!/usr/bin/env python

from fabric.api import *

"""
Base configuration
"""
env.project_name = 'vote'
env.user = 'root'
env.repo_path = '/home/canivote/can-i-vote/%(project_name)s' % env

"""
Environments
"""
def prod():
    env.hosts = ['198.61.200.10']

"""
Commands
"""

def git_pull(release):
    with cd(env.path):
        run('git pull origin %s' % release)

def restart():
		with cd(env.path):
			run('' % env)
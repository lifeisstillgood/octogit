"""
octogit

this file contains all the helper cli commands for octogit

"""
import os
import re
import sys

from pbs import git
from clint import args
from clint.textui import colored, puts, indent

from .core import get_repository, get_issues


def get_help():
    puts('How to octogit:')
    with indent(4):
        puts(colored.cyan('octogit create <repo>'))
        puts(colored.cyan('octogit delete <repo>'))
        puts(colored.cyan('octogit pull <repo>'))


def version():
    puts('development 0.1.0')


def git_status():
    print git.status()

def get_username_and_repo(url):
    import pdb; pdb.set_trace()
    # matching origin of this type 
    # http://www.github.com/myusuf3/delorean
    m = re.match("^.+?github.com/([a-zA-Z0-9_-]*)/([a-zA-Z0-9_-]*)\/?$", url)
    if m:
        return m.groups()
    else:
        # matching origin of this type
        # git@github.com:myusuf3/delorean.git
        username_repo = url.split(':')[1].replace('.git', '').split('/')
        if len(username_repo) == 2:
            return username_repo
        else:
            # matching url of this type
            # git://github.com/myusuf3/delorean.git
            username_repo = url.split('/')[3:]
            username_repo[1]=username_repo[1].replace('.git', '')
            return username_repo


def show_boating():
    puts('{0} by Mahdi Yusuf <@myusuf3>'.format(colored.yellow('octogit')))
    puts('{0} http://github.com/myusuf3/octogit'.format(colored.yellow('source')))

def find_github_remote(repository):
    remotes = repository.remotes
    for remote in remotes:
        if 'github' in remote.url:
            return remote.url
        else:
            pass
    puts(colored.red('This repository has no Github remotes')) 
    sys.exit(0)

def begin():
    if args.flags.contains(('--version', '-v')):
        version()
        sys.exit(0)

    elif args.get(0) == None:
        show_boating()

    elif args.get(0) == 'status':
        git_status()
        sys.exit(0)

    elif args.flags.contains(('--help', '-h')) or args.get(0) == 'help':
        get_help()
        sys.exit(0)

    elif args.flags.contains(('--issues', '-i')) or args.get(0) == 'issues':
        repo = get_repository()
        url = find_github_remote(repo)
        username, url = get_username_and_repo(url)
        get_issues(username, url)
        sys.exit(0)

    elif args.flags.contains(('--location', '-l')) or args.get(0) == 'location' :
        repo = get_repository()

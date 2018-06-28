# -*- coding: utf-8 -*-

""" A light git interface in python of the basic command.
    
    Does not work with git version prior to 2.7"""


import os
import subprocess
import locale

from urllib.parse import urlparse


# Can be override to specify git language. Should be in the form 'lang.encoding'.
# For instance : 'en-US.UTF-8'
GIT_LANG = '.'.join(locale.getdefaultlocale())



class NotInRepositoryError(Exception):
    pass



def in_repository(path):
    """Return True if path is inside a repository, False if not."""
    cwd = os.getcwd()
    
    try:
        os.chdir(path) if os.path.isdir(path) else os.chdir(os.path.dirname(path))
        cmd = 'git rev-parse 2> /dev/null > /dev/null'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.communicate()
    finally:
        os.chdir(cwd)
    
    return p.returncode == 0


def add(path):
    """Add the file pointed by path to the index.
    
    if path point to a directory, update the index to match the current state of the directory as
    a whole
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path) if os.path.isdir(path) else os.chdir(os.path.dirname(path))
        cmd = "LANGUAGE=" + GIT_LANG + " git add " + path
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def commit(path, log):
    """Record changes to the repository using log and -m option.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path) if os.path.isdir(path) else os.chdir(os.path.dirname(path))
        cmd = "LANGUAGE=" + GIT_LANG + " git commit " + path + " -m " + '"' + log + '"'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def checkout(path, branch=None, new=False):
    """Switch branches or restore working tree files.
    
    Parameter:
        path: (str)
            if no branch given - Path to the entry wich should be restored.
            if branch is given - Path from where git checkout command will be executed.
        branch: (str) name of the branch which we should checkout to
        new: (bool) Wheter we should create a new branch (True) or not (False)
    
    
    Restore working tree files pointed by path if no <branch> is given.
    Switch to <branch> if provided, creating it if new is True.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path) if os.path.isdir(path) else os.chdir(os.path.dirname(path))
        cmd = ("LANGUAGE=" + GIT_LANG + " git checkout " + path if not branch
                else "LANGUAGE=" + GIT_LANG + " git checkout " + branch if not new
                    else "LANGUAGE=" + GIT_LANG + " git checkout -b " + branch)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def status(path):
    """Show the working tree status.
    
    Parameter:
        url : (str) path to the repository
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path)
        print(GIT_LANG)
        cmd = "LANGUAGE=" + GIT_LANG + " git status"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def branch(path):
    """List branches.
    
    Parameter:
        url : (str) path to the repository
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path)
        cmd = "LANGUAGE=" + GIT_LANG + " git branch"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def current_branch(path):
    """Get current branch name
    
    Parameter:
        url : (str) path to the repository
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path)
        cmd = "LANGUAGE=" + GIT_LANG + " git rev-parse --abbrev-ref HEAD"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def reset(path, mode="mixed", commit='HEAD'):
    """Reset current HEAD to the specified state.
    
    Parameter:
        path   : (str) path the the entry we should be reset.
        mode   : (str) Mode for the reset, should be 'soft', 'mixed', 'hard', 'merge' or 'keep'.
        commit : (str) To which commit the reset shoul be done. Must be a commit's hash, 'HEAD' for
                       the last commit, to which '~' or '^' can be appended to choose ancestor or
                       parent.
    
    Resets the current branch head to <commit>
    and possibly updates the index (resetting it to the tree of <commit>) and the working tree
    depending on <mode>. if <mode> is omitted, defaults to "mixed". The <mode> must be one of the
    following:
        - soft
            Does not touch the index file or the working tree at all (but resets the
            head to <commit>, just like all modes do). This leaves all your changed files
            "Changes to be committed", as git status would put it.
        - mixed
            Resets the index but not the working tree (i.e., the changed files are preserved
            but not marked for commit) and reports what has not been updated. This is the
            default action.
        - hard
            Resets the index and working tree. Any changes to tracked files in the working tree
            since <commit> are discarded.
        - merge
            Resets the index and updates the files in the working tree that are different
            between <commit> and HEAD, but keeps those which are different between the index
            and working tree (i.e. which have changes which have not been added). If a file
            that is different between <commit> and the index has unstaged changes, reset is aborted.
        - keep
            Resets index entries and updates files in the working tree that are different
            between <commit> and HEAD. If a file that is different between <commit> and HEAD
            has local changes, reset is aborted.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    if mode and mode not in ["soft", "mixed", "hard", "merge", "keep"]:
        raise ValueError("Mode must be one of the following: "
                       + "'soft', 'mixed', 'hard', 'merge' or 'keep'.")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path) if os.path.isdir(path) else os.chdir(os.path.dirname(path))
        cmd = "LANGUAGE=" + GIT_LANG + " git reset --" + mode + " " + commit
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def pull(path, url, username=None, password=None):
    """Fetch from and integrate with another repository or a local branch.
    
    Parameter:
        path : (str) Path from where git pull command will be executed
        url  : (str) URL of the remote
        username : (str) Username for authentification if repository is private
        password : (str) Password for authentification if repository is private
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path)
        
        if username and password:
            url = urlparse(url)
            cmd = ("LANGUAGE=" + GIT_LANG
                 + "git pull " + url.scheme + "://" + username + ":" + password
                 + "@" + url.netloc + url.path)
        elif not (username or password):
            cmd = "LANGUAGE=" + GIT_LANG + " GIT_TERMINAL_PROMPT=0 git pull"
        else:
            raise ValueError("Password must be provided if username is given" if username
                             else "Username must be provided if password is given")
                        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        
        out = out.decode()
        err = err.decode()
        if password:
            out = out.replace(password, "•" * len(password))
            err = err.replace(password, "•" * len(password))
            
    finally:
        os.chdir(cwd)
    
    if p.returncode and "terminal prompts disabled" in err:
        return return_code, out, "Repository is private, please provide credentials"
    return (p.returncode, out, err)


def push(path, url, username=None, password=None):
    """Update remote refs along with associated objects.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path)
        
        ret, branch, err = current_branch(path)
        if ret:  # pragma: no cover
            return (ret, branch, "Couldn't retrieve current branch name \n".encode() + err)
        
        if username and password:
            url = urlparse(url)
            cmd = ("LANGUAGE=" + GIT_LANG + " git push "
                 + url.scheme + "://" + username + ":" + password + "@" + url.netloc + url.path)
        elif not (username or password):
            cmd = "LANGUAGE=" + GIT_LANG + " GIT_TERMINAL_PROMPT=0 git push"
        else:
            raise ValueError("Password must be provided if username is given" if username
                             else "Username must be provided if password is given")
            
        cmd += " -u origin " + branch
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        
        out = out.decode()
        err = err.decode()
        if password:
            out = out.replace(password, "•" * len(password))
            err = err.replace(password, "•" * len(password))
            
    finally:
        os.chdir(cwd)
    
    if p.returncode and "terminal prompts disabled" in err:
        return return_code, out, "Repository is private, please provide credentials"
    return (p.returncode, out, err)


def clone(path, url, to=None, username=None, password=None):
    """Clone a repository into a new directory.
    
    Parameter:
        path : (str) Path from where git clone command will be executed
        url  : (str) URL of the repository
        to   : (str) Directory to which clone the repository, default is repository's name
        username : (str) Username for authentification if repository is private
        password : (str) Password for authentification if repository is private
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are decoded in UTF-8"""
    if not in_repository(path):
        raise NotInRepositoryError("'" + path + "' is not inside a repository")
    
    cwd = os.getcwd()
    
    try:
        os.chdir(path)
        
        if username and password:
            url = urlparse(url)
            cmd = ("LANGUAGE=" + GIT_LANG
                 + "git clone " + url.scheme + "://" + username + ":" + password
                 + "@" + url.netloc + url.path)
        elif not (username or password):
            cmd = "LANGUAGE=" + GIT_LANG + " GIT_TERMINAL_PROMPT=0 git clone " + url
        else:
            raise ValueError("Password must be provided if username is given" if username
                             else "Username must be provided if password is given")
        
        if to:
            cmd += " " + to
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        
        out = out.decode()
        err = err.decode()
        if password:
            out = out.replace(password, "•" * len(password))
            err = err.replace(password, "•" * len(password))
            
    finally:
        os.chdir(cwd)
    
    if p.returncode and "terminal prompts disabled" in err:
        return return_code, out, "Repository is private, please provide credentials"
    return (p.returncode, out, err)

# -*- coding: utf-8 -*-

""" A light git interface in python of the basic command.
    
    Does not work with git version prior to 2.7"""


import os
import subprocess
import locale

from urllib.parse import urlparse


GIT_LANG = '.'.join(locale.getdefaultlocale())


def add(path):
    """Add the file pointed by path to the index.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
    
    cwd = os.getcwd()
    
    try:
        os.chdir(os.path.dirname(path))
        cmd = "LANGUAGE=" + GIT_LANG + " git add " + os.path.basename(path)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def commit(path, log):
    """Record changes to the repository using log and -m option.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
    
    cwd = os.getcwd()
    
    try:
        os.chdir(os.path.dirname(path))
        cmd = "LANGUAGE=" + GIT_LANG + " git commit -m " + '"' + log + '"'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def checkout(path, branch=None, new=False):
    """Switch branches or restore working tree files.
    
    Switch to <branch> if provided, creating it if new is True.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
    cwd = os.getcwd()
    
    try:
        os.chdir(os.path.dirname(path)) if not branch else os.chdir(path)
        cmd = ("LANGUAGE=" + GIT_LANG + " git checkout " + os.path.basename(path) if not branch
                else "LANGUAGE=" + GIT_LANG + " git checkout " + branch if not new
                    else "LANGUAGE=" + GIT_LANG + " git checkout -b " + branch)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def status(path):
    """Show the working tree status.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
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
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
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
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
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
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
    cwd = os.getcwd()
    
    if mode and mode not in ["soft", "mixed", "hard", "merge", "keep"]:
        raise ValueError("Mode must be one of the following: "
                       + "'soft', 'mixed', 'hard', 'merge' or 'keep'.")
    
    try:
        os.chdir(path)
        cmd = "LANGUAGE=" + GIT_LANG + " git reset --" + mode + " " + commit
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
    finally:
        os.chdir(cwd)
    
    return (p.returncode, out.decode(), err.decode())


def pull(path, url, username=None, password=None):
    """Fetch from and integrate with another repository or a local branch.
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
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
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
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
    
    Return:
        (return_code, stdout, stderr), both stderr and stdout are bytes"""
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

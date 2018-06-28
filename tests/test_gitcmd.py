# -*- coding: utf-8 -*-

import os
import unittest
import shutil
import subprocess

from gitcmd import gitcmd



gitcmd.GIT_LANG = 'en_US.UTF-8'

HOST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "host")
LOCAL_DIRS = os.path.join(os.path.dirname(os.path.realpath(__file__)), "local/")

def command(cmd):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    out, err = p.communicate()
    if p.returncode:
        raise RuntimeError("Return code : " + str(p.returncode) + " - " + err.decode() + out.decode())


class TestGitcmd(unittest.TestCase):
    
    def setUp(self):
        if os.path.isdir(HOST_DIR):
            shutil.rmtree(HOST_DIR)
        if os.path.isdir(LOCAL_DIRS):
            shutil.rmtree(LOCAL_DIRS)
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local,'file.txt')
        os.makedirs(LOCAL_DIRS)
        
        cwd = os.getcwd()
        command('git init --bare ' + HOST_DIR)
        command('git init ' + local)
        os.chdir(local)
        command('git config user.email "you@example.com"')
        command('git config user.name "Your Name"')
        command('git remote add origin ' + HOST_DIR)
        command('touch ' + test_file)
        command('git add ' + test_file)
        command('git commit ' + test_file + ' -m "test"')
        command('git push --set-upstream origin master')
        os.chdir(cwd)
    
    
    def tearDown(self):
        shutil.rmtree(HOST_DIR)
        shutil.rmtree(LOCAL_DIRS)
    
    
    def test0100_clone(self):
        self.assertEqual(0, gitcmd.clone(LOCAL_DIRS, HOST_DIR)[0])
        self.assertTrue(os.path.isdir(os.path.join(LOCAL_DIRS, 'host')))
    
    
    def test0101_clone_to(self):
        self.assertEqual(0, gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='test')[0])
        self.assertTrue(os.path.isdir(os.path.join(LOCAL_DIRS, 'test')))
    
    
    def test0102_clone_need_credentials(self):
        pass #TODO: Testing access denied by a private repository when not providing credentials
    
    
    def test0103_clone_credentials(self):
        pass #TODO: Testing access to a private repository when providing credentials
    
    
    def test0200_add(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        open(test_file, 'w+').close()
        ret, out, err = gitcmd.add(test_file)
        
        self.assertEqual(ret, 0)
        self.assertEqual(out, "")
    
    
    def test0201_add_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.add(test_file)
    
    
    def test0300_commit(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        open(test_file, 'w+').close()
        gitcmd.add(test_file)
        ret, out, err = gitcmd.commit(test_file, 'test')
        
        self.assertEqual(ret, 0)
        self.assertTrue(
            "test\n 1 file changed, 0 insertions(+), 0 deletions(-)\n create mode 100644 test\n"
            in out
        )
    
    
    def test0301_commit_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.commit('/tmp', 'log')
    
    
    def test0400_status_clean(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        ret, out, err = gitcmd.status(local)
        
        self.assertEqual(ret, 0)
        self.assertTrue('nothing to commit' in out)
    
    
    def test0401_status_to_add(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        open(test_file, 'w+').close()
        ret, out, err = gitcmd.status(local)
        
        self.assertEqual(ret, 0)
        self.assertTrue('Untracked files:' in out)
    
    
    def test0402_status_to_commit(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        open(test_file, 'w+').close()
        gitcmd.add(test_file)
        ret, out, err = gitcmd.status(local)
        
        self.assertEqual(ret, 0)
        self.assertTrue('Changes to be committed:' in out)
    
    
    def test0403_status_to_commit(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        open(test_file, 'w+').close()
        gitcmd.add(test_file)
        gitcmd.commit(test_file, 'test')
        ret, out, err = gitcmd.status(local)
        
        self.assertEqual(ret, 0)
        self.assertTrue('Your branch is ahead of \'origin/master\' by 1 commit.' in out)
    
    
    def test0404_status_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.status('/tmp')
    
    
    def test0500_push(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        open(test_file, 'w+').close()
        gitcmd.add(test_file)
        gitcmd.commit(test_file, 'test')
        ret, out, err = gitcmd.push(local, HOST_DIR)
        
        self.assertEqual(ret, 0)
        self.assertEqual(
            ("Branch 'master' set up to track remote branch 'master' ".replace("'", '')
                + "from 'origin'.\n".replace("'", '')),
            out
        )
    
    
    def test0501_push_need_credentials(self):
        pass #TODO: Testing access denied by a private repository when not providing credentials
    
    
    def test0502_push_credentials(self):
        pass #TODO: Testing access to a private repository when providing credentials
    
    
    def test0503_push_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.push('/tmp', 'url')
    
    
    def test0600_branch(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        open(test_file, 'w+').close()
        gitcmd.add(test_file)
        gitcmd.commit(test_file, 'test')
        gitcmd.push(local, HOST_DIR)
        
        ret, out, err = gitcmd.branch(local)
        self.assertEqual(ret, 0)
        self.assertEqual(out, "* master\n")
    
    
    def test0601_branch_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.branch('/tmp')
    
    
    def test0700_checkout(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        with open(os.path.join(local,'file.txt'), 'w+') as f:
            print("test", file=f)
        ret, out, err = gitcmd.status(local)
        self.assertEqual(ret, 0)
        self.assertTrue("Changes not staged for commit" in out)
        ret, out, err = gitcmd.checkout(os.path.join(local,'file.txt'))
        self.assertEqual(ret, 0)
        ret, out, err = gitcmd.status(local)
        self.assertTrue("working tree clean" in out)
    
    
    def test0701_checkout_new_branch(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        ret, out, err = gitcmd.checkout(local, 'test_branch', True)
        self.assertEqual(ret, 0)
        self.assertEqual("Switched to a new branch 'test_branch'\n", err)
        ret, out, err = gitcmd.branch(local)
        self.assertEqual("  master\n* test_branch\n", out)
    
    
    def test0702_checkout_branch(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        gitcmd.checkout(local, 'test_branch', True)
        gitcmd.branch(local)
        gitcmd.checkout(local, 'master')
        ret, out, err = gitcmd.branch(local)
        self.assertEqual(ret, 0)
        self.assertEqual("* master\n  test_branch\n", out)
    
    
    def test0703_checkout_nonexistent_branch(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        ret, out, err = gitcmd.checkout(local, 'test_branch')
        self.assertEqual(ret, 1)
        self.assertTrue("pathspec 'test_branch' did not match any file(s) known to git." in err)
    
    
    def test0704_checkout_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.checkout('/tmp')
    
    
    def test0800_current_branch(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        ret, out, err = gitcmd.current_branch(local)
        self.assertEqual(ret, 0)
        self.assertEqual(out, "master\n")
        gitcmd.checkout(local, branch="test_branch", new=True)
        ret, out, err = gitcmd.current_branch(local)
        self.assertEqual(ret, 0)
        self.assertEqual(out, "test_branch\n")
    
    
    def test801_current_branch_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.current_branch('/tmp')
    
    
    def test0900_reset(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        with open(os.path.join(local,'file.txt'), 'w+') as f:
            print("test", file=f)
        gitcmd.add(os.path.join(local,'file.txt'))
        ret, out, err = gitcmd.status(local)
        self.assertEqual(ret, 0)
        self.assertTrue("Changes to be committed" in out)
        ret, out, err = gitcmd.reset(local)
        self.assertEqual(ret, 0)
        self.assertEqual("Unstaged changes after reset:\nM\tfile.txt\n", out)
        ret, out, err = gitcmd.status(local)
        self.assertEqual(ret, 0)
        self.assertTrue("Changes not staged for commit:" in out)
    
    
    def test0902_reset_value_error(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        test_file = os.path.join(local, 'test')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        with self.assertRaises(ValueError):
            gitcmd.reset(local, mode="error")
    
    
    def test0903_reset_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.branch('/tmp')
    
    
    def test1000_pull(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        local2 = os.path.join(LOCAL_DIRS, 'local2')
        test_file = os.path.join(local, 'testfile')
        test_file2 = os.path.join(local, 'testfile')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local2')
        open(test_file, 'w+').close()
        gitcmd.add(test_file)
        gitcmd.commit(test_file, 'test')
        gitcmd.push(local, HOST_DIR)
        ret, out, err = gitcmd.pull(local2, HOST_DIR)
        self.assertEqual(ret, 0)
        self.assertTrue("Fast-forward\n testfile" in out)
        self.assertTrue(os.path.isfile(test_file2))
    
    
    def test1001_pull_useless(self):
        local = os.path.join(LOCAL_DIRS, 'local')
        local2 = os.path.join(LOCAL_DIRS, 'local2')
        test_file = os.path.join(local, 'testfile')
        test_file2 = os.path.join(local, 'testfile')
        
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local')
        gitcmd.clone(LOCAL_DIRS, HOST_DIR, to='local2')
        ret, out, err = gitcmd.pull(local2, HOST_DIR)
        self.assertEqual(ret, 0)
        self.assertEqual("Already up to date.\n", out.replace('-', ' '))
    
    
    def test1002_pull_need_credentials(self):
        pass #TODO: Testing access denied by a private repository when not providing credentials
    
    
    def test1003_pull_credentials(self):
        pass #TODO: Testing access to a private repository when providing credentials
    
    
    def test0901_pull_exception(self):
        with self.assertRaises(gitcmd.NotInRepositoryError):
            gitcmd.pull('/tmp', 'url')

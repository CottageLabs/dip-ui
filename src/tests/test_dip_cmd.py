# !/usr/bin/env python

"""
dipconfig.py - manage dip configuration
"""

from __future__ import print_function

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2013-2014, University of Oxford"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import sys
import os
import os.path
import re
import argparse
import logging
import errno
import StringIO
import shutil

log = logging.getLogger(__name__)

from unittest   import TestCase

from dip.dip    import DIP

if __name__ == "__main__":
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)

print("sys.path[0]: "+sys.path[0])

from dipcmd                 import diperrors
from dipcmd.dipmain         import runCommand
from dipcmd.dipconfig       import dip_get_default_dir

from tests.StdoutContext    import SwitchStdout, SwitchStderr
from tests.SetcwdContext    import ChangeCurrentDir

BASE_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test/data")
BASE_CONFIG = os.path.join(BASE_DIR, "config")
BASE_DIPDIR = os.path.join(BASE_DIR, "dipdir")

class TestDipCmd(TestCase):

    def setUp(self):
        self._dipdir = BASE_DIPDIR
        self._cnfdir = BASE_CONFIG
        if self._dipdir.startswith(BASE_DIR) and os.path.isdir(self._dipdir):
            shutil.rmtree(self._dipdir)
        return
        
    def tearDown(self):
        if self._dipdir.startswith(BASE_DIR):
            # shutil.rmtree(self._dipdir)
            pass
        return

    # Support functions

    def fpath(self, ref):
        return os.path.join(BASE_DIR, ref)

    def dpath(self, ref):
        return os.path.join(self._dipdir, ref)

    def create_test_dip(self, dipref="testdip"):
        dipdir = self.dpath(dipref)
        # create
        argv   = ["dip", "create", "--dip", dipref]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        return dipdir

    def create_populate_test_dip(self, dipref="testdip"):
        dipdir = self.create_test_dip(dipref=dipref)
        filespath  = self.fpath("files")
        argv   = ["dip", "--recursive", "add-files", filespath]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        return dipdir

    def assertFilesInDip(self, filespresent=[], filesabsent=[]):
        argv   = ["dip", "show"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** files in DIP *****\n%s*****"%result)
        for f in filespresent:
            p = self.fpath(f)
            self.assertIn(" %s"%p, result)
        for f in filesabsent:
            p = self.fpath(f)
            self.assertNotIn(" %s"%p, result)
        return

    # Tests

    def test_01_dip_create(self):
        dipdir = os.path.join(self._dipdir, "testdip")
        argv = ["dip", "create", "--dip", "testdip"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        self.assertTrue(os.path.isdir(dipdir))
        self.assertEqual(dip_get_default_dir(self._cnfdir), self._dipdir+"/testdip")
        self.assertEqual(
            outstr.getvalue(),
            "Created deposit information package at %s\n"%(dipdir)
            )
        # again...
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            with SwitchStderr(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_EXISTS)
        self.assertEqual(
            outstr.getvalue(),
            "Specified directory already exists: %s\n"%(dipdir)
            )
        return

    def test_02_dip_use(self):
        dipdir = os.path.join(self._dipdir, "testdip")
        argv = ["dip", "use", "--dip", "testdip"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            with SwitchStderr(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_NOTEXISTS)
        self.assertEqual(
            outstr.getvalue(),
            "Specified directory does not exist: %s\n"%(dipdir)
            )
        # create directory but no content
        os.makedirs(dipdir)
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            with SwitchStderr(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_NODIPHERE)
        self.assertEqual(
            outstr.getvalue(),
            "Specified directory does not contain a deposit information package: %s\n"%(dipdir)
            )
        shutil.rmtree(dipdir)
        # create
        newdir = self.create_test_dip("testdip")
        self.assertEqual(newdir, dipdir)
        # again...
        argv = ["dip", "use", "--dip", "testdip"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        self.assertEqual(outstr.getvalue(), "%s\n"%(dipdir))
        # again...
        argv = ["dip", "use"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        self.assertEqual(outstr.getvalue(), "%s\n"%(dipdir))
        return

    def test_03_dip_show(self):
        # create
        dipdir = self.create_test_dip("testdip")
        # show
        argv   = ["dip", "show"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Deposit information package at %s"%dipdir, result)
        self.assertIn("Files:", result)
        self.assertIn("Metadata files:", result)
        self.assertIn("%s/metadata/dcterms.xml (dcterms)"%dipdir, result)
        self.assertIn("Dublin Core:", result)
        self.assertIn("Endpoints:", result)
        return

    def test_04_dip_remove(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # show
        argv   = ["dip", "remove", "--dip", "testdip"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        # confirm removed
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        self.assertFalse(os.path.isdir(dipdir))
        return

    def test_10_dip_add_file_single(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # add
        file1path = self.fpath("files/file1.txt")
        argv   = ["dip", "add-files", file1path]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** add-files *****\n%s*****"%result)
        self.assertIn("Adding files to deposit information package at %s ..."%(dipdir), result)
        self.assertIn("  %s"%file1path, result)
        # self.assertIn("Done.", result)
        # show
        argv   = ["dip", "show"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** show *****\n%s*****"%result)
        self.assertIn("Files:", result)
        self.assertIn(" %s"%file1path, result)
        return

    def test_11_dip_add_files_multi(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # add
        file1path = self.fpath("files/file1.txt")
        file2path = self.fpath("files/file2.txt")
        sub1path  = self.fpath("files/sub1")
        sub11path = self.fpath("files/sub1/sub11.txt")
        sub12path = self.fpath("files/sub1/sub12.txt")
        argv   = ["dip", "add-files", file1path, file2path, sub1path]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** add-files *****\n%s*****"%result)
        self.assertIn("Adding files to deposit information package at %s ..."%(dipdir), result)
        self.assertIn("  %s"%file1path, result)
        self.assertIn("  %s"%file2path, result)
        self.assertIn("  %s"%sub11path, result)
        self.assertIn("  %s"%sub12path, result)
        self.assertIn("Done.", result)
        # show
        argv   = ["dip", "show"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** show *****\n%s*****"%result)
        self.assertIn("Files:", result)
        self.assertIn(" %s"%file1path, result)
        self.assertIn(" %s"%file2path, result)
        self.assertIn(" %s"%sub11path, result)
        self.assertIn(" %s"%sub12path, result)
        return

    def test_12_dip_add_files_recursive(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # add
        filespath  = self.fpath("files")
        file1path  = self.fpath("files/file1.txt")
        file2path  = self.fpath("files/file2.txt")
        sub11path  = self.fpath("files/sub1/sub11.txt")
        sub12path  = self.fpath("files/sub1/sub12.txt")
        sub21path  = self.fpath("files/sub2/sub21.txt")
        sub22path  = self.fpath("files/sub2/sub22.txt")
        sub311path = self.fpath("files/sub3/sub31/sub311.txt")
        sub331path = self.fpath("files/sub3/sub33/sub331.txt")
        argv   = ["dip", "--recursive", "add-files", filespath]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** add-files *****\n%s*****"%result)
        self.assertIn("Adding files to deposit information package at %s ..."%(dipdir), result)
        self.assertIn("  %s"%file1path, result)
        self.assertIn("  %s"%file2path, result)
        self.assertIn("  %s"%sub11path, result)
        self.assertIn("  %s"%sub12path, result)
        self.assertIn("  %s"%sub21path, result)
        self.assertIn("  %s"%sub22path, result)
        self.assertIn("  %s"%sub311path, result)
        self.assertIn("  %s"%sub331path, result)
        self.assertIn("Done.", result)
        # show
        argv   = ["dip", "show"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        # print("***** show *****\n%s*****"%result)
        self.assertIn("Files:", result)
        self.assertIn(" %s"%file1path, result)
        self.assertIn(" %s"%file2path, result)
        self.assertIn(" %s"%sub11path, result)
        self.assertIn(" %s"%sub12path, result)
        self.assertIn(" %s"%sub21path, result)
        self.assertIn(" %s"%sub22path, result)
        self.assertIn(" %s"%sub311path, result)
        self.assertIn(" %s"%sub331path, result)
        return

    def test_13_dip_remove_file_single(self):
        # create
        dipdir = self.create_populate_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # Check files present
        self.assertFilesInDip(filespresent=["files/file1.txt", "files/file2.txt"])
        # Remove file
        file1path  = self.fpath("files/file1.txt")
        argv   = ["dip", "remove-file", "files/file1.txt"]
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Removing files from deposit information package at %s"%dipdir, result)
        self.assertIn("  %s"%file1path, result)
        # Check files present again
        self.assertFilesInDip(filesabsent=["files/file1.txt"], filespresent=["files/file2.txt"])
        return

    def test_14_dip_remove_file_multiple(self):
        # create
        dipdir = self.create_populate_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # Check files present
        self.assertFilesInDip(
            filespresent=[
                "files/file1.txt", "files/file2.txt", 
                "files/sub1/sub11.txt", "files/sub1/sub12.txt"
                ]
            )
        # Remove file
        argv   = ["dip", "remove-files", "files/file1.txt", "files/file2.txt", "files/sub1"]
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Removing files from deposit information package at %s"%dipdir, result)
        self.assertIn("  %s"%self.fpath("files/file1.txt"), result)
        self.assertIn("  %s"%self.fpath("files/file2.txt"), result)
        self.assertIn("  %s"%self.fpath("files/sub1/sub11.txt"), result)
        self.assertIn("  %s"%self.fpath("files/sub1/sub12.txt"), result)
        # Check files present again
        self.assertFilesInDip(
            filesabsent=[
                "files/file1.txt", "files/file2.txt", 
                "files/sub1/sub11.txt", "files/sub1/sub12.txt"
                ]
            )
        return

    def test_15_dip_remove_file_recursive(self):
        # create
        dipdir = self.create_populate_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # Check files present
        self.assertFilesInDip(
            filespresent=[
                "files/file1.txt", "files/file2.txt", 
                "files/sub1/sub11.txt", "files/sub1/sub12.txt",
                "files/sub2/sub21.txt", "files/sub2/sub22.txt",
                "files/sub3/sub31/sub311.txt",
                "files/sub3/sub33/sub331.txt"
                ]
            )
        # Remove file
        argv   = ["dip", "--recursive", "remove-files", "files/sub3"]
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Removing files from deposit information package at %s"%dipdir, result)
        self.assertIn("  %s"%self.fpath("files/sub3/sub31/sub311.txt"), result)
        self.assertIn("  %s"%self.fpath("files/sub3/sub33/sub331.txt"), result)
        # Check files present again
        self.assertFilesInDip(
            filespresent=[
                "files/file1.txt", "files/file2.txt", 
                "files/sub1/sub11.txt", "files/sub1/sub12.txt",
                "files/sub2/sub21.txt", "files/sub2/sub22.txt"
                ],
            filesabsent=[
                "files/sub3/sub31/sub311.txt",
                "files/sub3/sub33/sub331.txt"
                ]
            )
        return

    def test_20_dip_add_show_attributes(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # Test attributes
        argvshow   = (
            [ "dip", "show-attributes"
            , "dc:creator"
            , "dc:created"
            , "dc:title"
            , "dc:identifier"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvshow)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertNotIn("dc:creator",      result)
        self.assertNotIn("dc:created",      result)
        self.assertNotIn("dc:title",        result)
        self.assertNotIn("dc:identifier",   result)
        # Add attributes
        argvset   = (
            [ "dip", "add-attributes"
            , "dc:creator=John Smith", "dc:creator=Tom Jones"
            , "dc:created=2014-01-01"
            , '''dc:title="Smith and Jones' package"'''
            , "dc:identifier=testdip/123456789"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvset)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Adding attributes to deposit information package at %s"%dipdir, result)
        self.assertIn('''  dc:creator="John Smith"''',              result)
        self.assertIn('''  dc:creator="Tom Jones"''',               result)
        self.assertIn('''  dc:created="2014-01-01"''',              result)
        self.assertIn('''  dc:title="Smith and Jones' package"''',  result)
        self.assertIn('''  dc:identifier="testdip/123456789"''',    result)
        # Test attributes again
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvshow)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn('''dc:creator="John Smith"''',              result)
        self.assertIn('''dc:creator="Tom Jones"''',               result)
        self.assertIn('''dc:created="2014-01-01"''',              result)
        self.assertIn('''dc:title="Smith and Jones' package"''',  result)
        self.assertIn('''dc:identifier="testdip/123456789"''',    result)
        return

    def test_21_dip_remove_attributes(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # Add attributes
        argvset   = (
            [ "dip", "add-attributes"
            , "dc:creator=John Smith", "dc:creator=Tom Jones"
            , "dc:created=2014-01-01"
            , '''dc:title="Smith and Jones' package"'''
            , "dc:identifier=testdip/123456789"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvset)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        # Test attributes
        argvshow   = (
            [ "dip", "show-attributes"
            , "dc:creator"
            , "dc:created"
            , "dc:title"
            , "dc:identifier"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvshow)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn('''dc:creator="John Smith"''',              result)
        self.assertIn('''dc:creator="Tom Jones"''',               result)
        self.assertIn('''dc:created="2014-01-01"''',              result)
        self.assertIn('''dc:title="Smith and Jones' package"''',  result)
        self.assertIn('''dc:identifier="testdip/123456789"''',    result)
        # Remove some attributes
        argvremove   = (
            [ "dip", "remove-attributes"
            , "dc:creator"
            , "dc:title"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvremove)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Removing attributes from deposit information package at %s"%dipdir, result)
        self.assertIn('''  dc:creator''',   result)
        self.assertIn('''  dc:title''',     result)
        # Test attributes again
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvshow)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn('''dc:created="2014-01-01"''',                result)
        self.assertIn('''dc:identifier="testdip/123456789"''',      result)
        self.assertNotIn('''dc:creator="John Smith"''',             result)
        self.assertNotIn('''dc:creator="Tom Jones"''',              result)
        self.assertNotIn('''dc:title="Smith and Jones' package"''', result)
        return

    def test_22_dip_update_attributes(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # Add attributes
        argvset   = (
            [ "dip", "add-attributes"
            , "dc:creator=John Smith"
            , "dc:created=2014-01-01"
            , '''dc:title="Smith and Jones' package"'''
            , "dc:identifier=testdip/123456789"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvset)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        # Test attributes
        argvshow   = (
            [ "dip", "show-attributes"
            , "dc:creator"
            , "dc:created"
            , "dc:title"
            , "dc:identifier"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvshow)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn('''dc:creator="John Smith"''',                result)
        self.assertNotIn('''dc:creator="Tom Jones"''',              result)
        self.assertIn('''dc:created="2014-01-01"''',                result)
        self.assertIn('''dc:title="Smith and Jones' package"''',    result)
        self.assertIn('''dc:identifier="testdip/123456789"''',      result)
        # Update some attributes
        argvupdate   = (
            [ "dip", "add-attributes"
            , "dc:creator=Tom Jones"
            , "dc:created=2014-04-02"
            ])
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvupdate)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn("Adding attributes to deposit information package at %s"%dipdir, result)
        self.assertIn('''  dc:creator="Tom Jones"''',               result)
        self.assertIn('''  dc:created="2014-04-02"''',              result)
        # Test attributes again
        outstr = StringIO.StringIO()
        with ChangeCurrentDir(BASE_DIR):
            with SwitchStdout(outstr):
                status = runCommand(self._cnfdir, self._dipdir, argvshow)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        result = outstr.getvalue()
        self.assertIn('''dc:creator="John Smith"''',                result)
        self.assertIn('''dc:creator="Tom Jones"''',                 result)
        self.assertIn('''dc:created="2014-04-02"''',                result)
        self.assertNotIn('''dc:created="2014-01-01"''',             result)
        self.assertIn('''dc:title="Smith and Jones' package"''',    result)
        self.assertIn('''dc:identifier="testdip/123456789"''',      result)
        return

if __name__ == "__main__":
    import nose
    nose.run()

# End.


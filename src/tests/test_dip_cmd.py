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

    def create_test_dip(self, dipref="testdip"):
        dipdir = os.path.join(self._dipdir, dipref)
        # create
        argv   = ["dip", "create", "--dip", dipref]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, diperrors.DIP_SUCCESS)
        return dipdir

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

    def test_05_dip_add_file_single(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # add
        file1path = os.path.join(BASE_DIR, "files/file1.txt")
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

    def test_06_dip_add_files_multi(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # add
        file1path = os.path.join(BASE_DIR, "files/file1.txt")
        file2path = os.path.join(BASE_DIR, "files/file2.txt")
        sub1path  = os.path.join(BASE_DIR, "files/sub1")
        sub11path = os.path.join(BASE_DIR, "files/sub1/sub11.txt")
        sub12path = os.path.join(BASE_DIR, "files/sub1/sub12.txt")
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

    def test_07_dip_add_files_recursive(self):
        # create
        dipdir = self.create_test_dip("testdip")
        self.assertTrue(os.path.isdir(dipdir))
        # add
        filespath  = os.path.join(BASE_DIR, "files")
        file1path  = os.path.join(BASE_DIR, "files/file1.txt")
        file2path  = os.path.join(BASE_DIR, "files/file2.txt")
        sub11path  = os.path.join(BASE_DIR, "files/sub1/sub11.txt")
        sub12path  = os.path.join(BASE_DIR, "files/sub1/sub12.txt")
        sub21path  = os.path.join(BASE_DIR, "files/sub2/sub21.txt")
        sub22path  = os.path.join(BASE_DIR, "files/sub2/sub22.txt")
        sub311path = os.path.join(BASE_DIR, "files/sub3/sub31/sub311.txt")
        sub331path = os.path.join(BASE_DIR, "files/sub3/sub33/sub331.txt")
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

if __name__ == "__main__":
    import nose
    nose.run()

# End.


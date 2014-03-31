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

    def test_dip_create(self):
        argv = ["dip", "create", "--dip", "testdip"]
        outstr = StringIO.StringIO()
        with SwitchStdout(outstr):
            status = runCommand(self._cnfdir, self._dipdir, argv)
        self.assertEqual(status, 0)
        self.assertTrue(os.path.isdir(os.path.join(self._dipdir, "testdip")))
        self.assertEqual(dip_get_default_dir(self._cnfdir), self._dipdir+"/testdip")
        return

if __name__ == "__main__":
    import nose
    nose.run()

# End.


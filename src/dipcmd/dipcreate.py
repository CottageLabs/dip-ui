# !/usr/bin/env python

"""
dipcreate.py - create a deposit informaton package
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

log = logging.getLogger(__name__)

import dip

def dip_create(dipdir):
    """
    Create a deposit information package in the designated directory

    dipdir  is a filly qualified directyory name where the DIP is created.

    returns zero to indicate success, or a non-zero status code.
    """
    try:
        os.makedirs(dipdir)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            print("Specified directory already exists: %s"%(dipdir), file=sys.stderr)
        else:
            print("Error %d creating DIP directory: %s"%(exc.errno, dipdir), file=sys.stderr)
        return 2
    d = dip.DIP(dipdir)
    return 0

# End.
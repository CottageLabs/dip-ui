# !/usr/bin/env python

"""
diplocal.py - methods for manipulation of a local deposit informaton package
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
import shutil
import logging
import errno

log = logging.getLogger(__name__)

import dip

from dipcmd     import diperrors

def dip_create(dipdir):
    """
    Create a deposit information package in the designated directory

    dipdir  is a fully qualified directory name where the DIP is created.

    returns zero to indicate success, or a non-zero status code.
    """
    try:
        os.makedirs(dipdir)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            print("Specified directory already exists: %s"%(dipdir), file=sys.stderr)
            return diperrors.DIP_EXISTS
        else:
            print("Error %d creating DIP directory: %s"%(exc.errno, dipdir), file=sys.stderr)
        return exc.errno
    d = dip.DIP(dipdir)
    print("Created deposit information package at %s"%(dipdir))
    return diperrors.DIP_SUCCESS

def dip_use(dipdir, report_dir=True):
    """
    Use deposit information package in the designated directory

    dipdir  is a fully qualified directory name where a DIP is expected.

    returns zero to indicate success, or a non-zero status code.
    """
    if not os.path.isdir(dipdir):
        print("Specified directory does not exist: %s"%(dipdir), file=sys.stderr)
        return diperrors.DIP_NOTEXISTS
    if  ( not os.path.isfile(os.path.join(dipdir, "deposit.json")) or
          not os.path.isdir(os.path.join(dipdir, "metadata")) or
          not os.path.isdir(os.path.join(dipdir, "history")) or
          not os.path.isdir(os.path.join(dipdir, "packages")) or
          not os.path.isfile(os.path.join(dipdir, "metadata", "dcterms.xml"))
        ):
        print("Specified directory does not contain a deposit information package: %s"%(dipdir), file=sys.stderr)
        return diperrors.DIP_NODIPHERE
    if report_dir:
        print(dipdir)
    return diperrors.DIP_SUCCESS

def dip_show(dipdir):
    """
    Showe details of deposit information package in the designated directory

    dipdir  is a fully qualified directory name where a DIP is expected.

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    d   = dip.DIP(dipdir)
    print("Deposit information package at %s"%dipdir)

    print("Files:")
    dfs = d.get_files()
    for df in dfs:
        print("  %s %s"%(df.added, df.path))

    print("Metadata files:")
    mfs = d.get_metadata_files()
    for mf in mfs:
        print("  %s %s (%s)"%(mf.added, mf.path, mf.format))

    print("Dublin Core:")
    dcs = d.get_dublin_core()
    for dc in dcs:
        print("  %s"%dc)

    print("Endpoints:")
    eps = d.get_endpoints()
    for ep in eps:
        print("  %s"%ep)

    return diperrors.DIP_SUCCESS

def dip_remove(dipdir):
    """
    Remove a deposit information package in the designated directory

    dipdir  is a fully qualified directory name where the DIP is created.

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    shutil.rmtree(dipdir)
    print("Removed deposit information package at %s"%(dipdir))
    return diperrors.DIP_SUCCESS

def dip_add_files(dipdir, files, recursive=False):
    """
    Add filoes to a deposit information package.  E.g.

        dip add-file [--recursive] [--dip=<directory>] file, ...

    dipdir  is a fully qualified DIP directory name

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    print("Adding files to deposit information package at %s ..."%(dipdir))
    d   = dip.DIP(dipdir)
    for f in files:
        status = dip_add_files_subdir(d, dipdir, f, True, recursive)
        if status != diperrors.DIP_SUCCESS:
            break
    if len(files) > 1 or recursive:
        print("Done.")
    return status

def dip_add_files_subdir(dip, subdir, f, scan, recursive):
    """
    Auxilliary recursive helper function to process files and subdirectories

    scan        is True if the current directory is to be scanned
    recursive   is True if all nested directories are to be scanned
    """
    log.debug("dip_add_files_subdir: %s, %s"%(subdir, f))
    status = diperrors.DIP_SUCCESS
    p = os.path.join(subdir, f)
    if os.path.isdir(p):
        if scan:
            files = os.listdir(p)
            for f in files:
                status = dip_add_files_subdir(dip, p, f, recursive, recursive)
                if status != diperrors.DIP_SUCCESS:
                    break
    else:
        print("  %s"%p)
        dip.set_file(p)
    return status

# End.
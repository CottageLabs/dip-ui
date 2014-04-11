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
from diplocal   import dip_use

def dip_package(dipdir, basedir=None, format="http://purl.org/net/sword/package/SimpleZip"):
    """
    Create package for deposit from DIP contents.  Write name of package file to stdout.

    dipdir  is a fully qualified directory name where a DIP is expected.
    basedir is a base directory used for calculation of relative paths within the package

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    d = dip.DIP(dipdir)
    print("Packaging deposit information package at %s"%dipdir)
    z = d.package(package_format=format, basedir=basedir)
    print(z)
    return diperrors.DIP_SUCCESS

def dip_deposit(
            dipdir,
            collection_uri=None, servicedoc_uri=None, username=None, password=None,
            basedir=None, format="http://purl.org/net/sword/package/SimpleZip"
            ):
    if not servicedoc_uri:
        raise ValueError("@@TODO - service document discovery")
    if not username:
        print("No username provided for deposit operation", file=sys.stderr)
        return diperrors.DIP_NOUSERNAME
    if not password:
        print("No password provided for deposit operation", file=sys.stderr)
        return diperrors.DIP_NOPASSWORD
    d = dip.DIP(dipdir)
    print("Depositing deposit information package at %s"%dipdir)
    print("  collection_uri=%s"%collection_uri)
    print("  servicedoc_uri=%s"%servicedoc_uri)
    print("  username=%s"%username)
    print("  password=%s"%password)
    sss = dip.Endpoint(
        col_iri=collection_uri, 
        sd_iri=servicedoc_uri, 
        username=username,
        package=format
        )
    d.set_endpoint(endpoint=sss)
    d.deposit(sss.id, user_pass=password, basedir=basedir)
    return diperrors.DIP_SUCCESS

# End.
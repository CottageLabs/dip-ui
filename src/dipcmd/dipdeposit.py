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
    package_info = d.package(package_format=format, basedir=basedir)
    print(package_info.path)
    return diperrors.DIP_SUCCESS

def dip_deposit(
            dipdir,
            collection_uri=None, servicedoc_uri=None, username=None, password=None,
            basedir=None, format="http://purl.org/net/sword/package/SimpleZip"
            ):
    """
    In initiate deposit (currently completes synchronously, but future versions may
    return before final status of deposit is known).
    """
    # @@TODO support deposit from package file or dip(?)
    if not servicedoc_uri:
        raise ValueError("@@TODO - service document discovery")
    if not username:
        print("No username provided for deposit operation", file=sys.stderr)
        return diperrors.DIP_NOUSERNAME
    if not password:
        print("No password provided for deposit operation", file=sys.stderr)
        return diperrors.DIP_NOPASSWORD
    d = dip.DIP(dipdir)
    # print("Depositing deposit information package at %s"%dipdir)
    # print("  collection_uri=%s"%collection_uri)
    # print("  servicedoc_uri=%s"%servicedoc_uri)
    # print("  username=%s"%username)
    # print("  password=%s"%password)
    sss = dip.Endpoint(
        col_iri=collection_uri, 
        sd_iri=servicedoc_uri, 
        username=username,
        package=format
        )
    d.set_endpoint(endpoint=sss)
    # See: https://github.com/CottageLabs/dip/blob/master/tests/test_sss.py#L145
    cm, dr = d.deposit(sss.id, user_pass=password, basedir=basedir)
    if cm.response_code not in [200, 201]:
        print("SWORD deposit failed: %d"%cm.response_code)
        print(format_CommsMeta(cm))
        return diperrors.DIP_DEPOSITFAIL

    # print("********\n")
    # print(format_CommsMeta(cm))
    # print("********\n")
    # print(format_DepositReceipt(dr))
    # print("********\n")

    # find out the state of the deposit
    # print("******** states:\n")
    # statement = d.get_repository_statement(sss.id, user_pass=password) # gets a sword2.Statement object
    # states = statement.states   # the statement object provides access to the list of states the object is in
    # for term, description in states:
    #     print(term)      # the URI which represents the state the item is in
    #     print(description)   # a human readable description of the state (e.g. "It is in the Archive!")
    # print("********\n")

    print("token=%s"%(dr.id))
    return diperrors.DIP_SUCCESS

def dip_status(dipdir, token, collection_uri=None):
    """
    Determine status of previously submitted deposit requesrt.

    This command provides a route to future support of asynchronous deposit 
    completion.  For now, it is implemented as a query to a sybnchronously
    completed deposit operation.

    @@TODO: can we use the token to query the SSS status of the deposit>?
    """
    raise NotImplementedError("@@TODO - deposit status query")
    return

def format_CommsMeta(cm):
    txt    = "CommsMeta("
    fields = (
        ("method",          cm.method),
        ("request_url",     cm.request_url),
        ("response_code",   cm.response_code),
        ("username",        cm.username),
        # ("password",        cm.password),
        ("auth_type",       cm.auth_type),
        ("headers",         cm.headers)
        )
    sep= ""
    for label, value in fields:
        if value:
            txt += "%s%s=%s"%(sep, label, value)
            sep = ", "
    txt += ")"
    return txt

def format_DepositReceipt(dr):
    txt    = "DepositReceipt("
    fields = (
        ("title",               dr.title),
        ("id",                  dr.id),
        ("updated",             dr.updated),
        ("summary",             dr.summary),
        ("categories",          dr.categories),
        ("edit",                dr.edit),
        # ("edit_media",          dr.edit_media),
        # ("edit_media_feed",     dr.edit_media_feed),
        # ("alternate",           dr.alternate),
        # ("se_iri",              dr.se_iri),
        # ("cont_iri",            dr.cont_iri),
        # ("content",             dr.content),
        # ("links",               dr.links),
        # ("metadata",            dr.metadata),
        # ("packaging",           dr.packaging),
        # ("response_headers",    dr.response_headers),
        ("location",            dr.location)
        )
    sep= "\n    "
    for label, value in fields:
        if value:
            txt += "%s%s=%s"%(sep, label, value)
            sep = ",\n    "
    txt += "\n    )"
    return txt

# End.
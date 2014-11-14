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

def dip_visit_files(basedir, filepath, scan, recursive, visitfn):
    """
    Recursive helper function to process files and subdirectories

    If a file is specified, the visitor finction is applied to that file.

    If a directory is specified, its contents are visited in `scan` is True.

    basedir     is a base directory for resolving relative file references
    filepath    is a file or directory to be visited
    scan        is True if the current directory is to be scanned
    recursive   is True if all nested directories are to be scanned
    visitfn     is a visitor function to be applied to each visited file.

    Returns diperrors.DIP_SUCCESS, or the value from the first visitor function
    call that does not return return diperrors.DIP_SUCCESS.
    """
    # log.debug("dip_visit_files: %s, %s"%(basedir, filepath))
    p = os.path.join(basedir, filepath)
    if os.path.isdir(p):
        if scan:
            files = os.listdir(p)
            for f in files:
                status = dip_visit_files(p, f, recursive, recursive, visitfn)
                if status != diperrors.DIP_SUCCESS:
                    break
    else:
        status = visitfn(p)
    return status

def dip_add_files(dipdir, files, recursive=False, basedir=None):
    """
    Add files to a deposit information package.  E.g.

        dip [--recursive] [--dip=<directory>] add-file file ...

    dipdir      is a fully qualified DIP directory name
    files       is a list of files/directories to be added
    recursive   True if directories encountered are to be scanned recursively
                (otherwise) explicitly-mentioned directories are scanned
                just one level down.
    basedir     is a base directory for resolving relative file references

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    if not basedir:
        basedir = os.getcwd()
    print("Adding files to deposit information package at %s ..."%(dipdir))
    d   = dip.DIP(dipdir)
    for f in files:
        # -- visitor function
        def dip_set_file(p):
            d.set_file(p)
            print("  %s"%p)
            return diperrors.DIP_SUCCESS
        # --
        status = dip_visit_files(basedir, f, True, recursive, dip_set_file)
        if status != diperrors.DIP_SUCCESS:
            break
    if len(files) > 1 or recursive:
        print("Done.")
    return status

def dip_remove_files(dipdir, files, recursive=False, basedir=None):
    """
    Remove files from a deposit information package.  E.g.

        dip [--recursive] [--dip=<directory>] remove-file file ...

    dipdir      is a fully qualified DIP directory name
    files       is a list of files/directories to be removed from the DIP
    recursive   True if directories encountered are to be scanned recursively
                (otherwise) explicitly-mentioned directories are scanned
                just one level down.
    basedir     is a base directory for resolving relative file references

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    if not basedir:
        basedir = os.getcwd()
    print("Removing files from deposit information package at %s ..."%(dipdir))
    d   = dip.DIP(dipdir)
    for f in files:
        # -- visitor function
        def dip_remove_file(p):
            d.remove_file(p)
            print("  %s"%p)
            return diperrors.DIP_SUCCESS
        # --
        status = dip_visit_files(basedir, f, True, recursive, dip_remove_file)
        if status != diperrors.DIP_SUCCESS:
            break
    if len(files) > 1 or recursive:
        print("Done.")
    return status

def _check_attribute_name(aname):
    """
    Check attribute name, returning either a properties dictionary or None
    """
    attributes_allowed = (
        { 'dc:creator':     { 'multiple': True }
        , 'dc:created':     { 'multiple': False }
        , 'dc:title':       { 'multiple': False }
        , 'dc:identifier':  { 'multiple': False }
        })
    if aname not in attributes_allowed:
        print("Unrecognized attribute name: %s"%(aname), file=sys.stderr)
        return None
    return attributes_allowed[aname]

def dip_set_attributes(dipdir, attrs):
    """
    Add attributes to a deposit information package.

    dipdir      is a fully qualified DIP directory name
    attrs       is a list of attributes to be added.  Each attribute is
                a "name=value" string that is dismantles into attribute name
                and value to be added.

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    print("Adding attributes to deposit information package at %s ..."%(dipdir))
    d = dip.DIP(dipdir)
    for attr in attrs:
        #                            1    2      3 4     5
        attrvalre    = re.compile(r'^(\w+:(\w+))=("(.*)"|(.*))$')
        attrvalmatch = attrvalre.match(attr)
        if not attrvalmatch:
            print("Attribute name/value format is not valid: %s"%(attr), file=sys.stderr)
            return diperrors.DIP_INVALIDATTR
        aname = attrvalmatch.group(1)
        aterm = attrvalmatch.group(2)
        aval  = attrvalmatch.group(4) or attrvalmatch.group(5) or ""
        aprop = _check_attribute_name(aname)
        if not aprop:
            return diperrors.DIP_UNKNOWNATTR
        if not aprop['multiple']:
            d.remove_dublin_core(dcterm=aterm)
        d.add_dublin_core(aterm, aval)
        print('''  %s="%s"'''%(aname, aval.replace('"', '\\"')))
    # @@save here?
    return diperrors.DIP_SUCCESS

def dip_show_attributes(dipdir, attrs):
    """
    Display attributes from a deposit information package.

    dipdir      is a fully qualified DIP directory name
    attrs       is a list of attribute named to be displayed.

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    d = dip.DIP(dipdir)
    for attr in attrs:
        #                            1    2
        attrvalre    = re.compile(r'^(\w+:(\w+))$')
        attrvalmatch = attrvalre.match(attr)
        if not attrvalmatch:
            print("Attribute name format is not valid: %s"%(attr), file=sys.stderr)
            return diperrors.DIP_INVALIDATTR
        aname = attrvalmatch.group(1)
        aterm = attrvalmatch.group(2)
        aprop = _check_attribute_name(aname)
        if not aprop:
            return diperrors.DIP_UNKNOWNATTR
        avals = d.get_dublin_core(dcterm=aterm)
        for (t, v, l) in avals:
            print('''dc:%s="%s"'''%(t, v.replace('"', '\\"')))
    return status

def dip_remove_attributes(dipdir, attrs):
    """
    Display attributes from a deposit information package.

    dipdir      is a fully qualified DIP directory name
    attrs       is a list of attribute named to be displayed.

    returns zero to indicate success, or a non-zero status code.
    """
    status = dip_use(dipdir, report_dir=False)
    if status != diperrors.DIP_SUCCESS:
        return status
    print("Removing attributes from deposit information package at %s ..."%(dipdir))
    d = dip.DIP(dipdir)
    for attr in attrs:
        #                            1    2
        attrvalre    = re.compile(r'^(\w+:(\w+))$')
        attrvalmatch = attrvalre.match(attr)
        if not attrvalmatch:
            print("Attribute name format is not valid: %s"%(attr), file=sys.stderr)
            return diperrors.DIP_INVALIDATTR
        aname = attrvalmatch.group(1)
        aterm = attrvalmatch.group(2)
        aprop = _check_attribute_name(aname)
        if not aprop:
            return diperrors.DIP_UNKNOWNATTR
        avals = d.remove_dublin_core(dcterm=aterm)
        print('''  %s'''%(aname))
    return diperrors.DIP_SUCCESS

# End.
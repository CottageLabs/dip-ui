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
import json
import errno
import logging

log = logging.getLogger(__name__)

from collections        import namedtuple

from dipcmd             import diperrors

SwordService = namedtuple('SwordService', ['servicedoc_uri', 'collection_uri', 'username', 'password'])

CONFIGFILE = "dip_config.json"

def strip_quotes(val):
    if val and val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    return val

def get_dipdir(dip_config, dir):
    dipdir  = os.path.abspath(dir)
    dipbase = os.path.realpath(dip_config['dipbase'])
    log.debug("dipdir: dipdir  %s"%(dipdir))
    log.debug("dipdir: dipbase %s"%(dipbase))
    if ( os.path.isdir(dipdir) and 
         os.path.commonprefix([dipbase, os.path.realpath(dipdir)]) == dipbase):
       return dipdir
    return None

def configfilename(configbase):
    return os.path.abspath(os.path.join(configbase, CONFIGFILE))

def readconfig(configbase):
    """
    Read configuration in indicated directory and return as a dictionary
    """
    dip_config = (
        { "dipbase":  None
        , "dipdir":   None
        })
    configfile = None
    try:
        with open(configfilename(configbase), 'r') as configfile:
            dip_config = json.load(configfile)
            # log.debug("readconfig: %s"%(configfilename(configbase)))
            # log.debug("dip_config: %s"%([dip_config]))
    except IOError as exc: # Python >2.5
        if exc.errno == errno.ENOENT:
            pass    # Ignore file not exists for now
        else:
            raise
    return dip_config

def writeconfig(configbase, config):
    """
    Write supplied configuration dictionary to indicated directory
    """
    try:
        os.makedirs(configbase)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(configbase):
            pass
        else:
            raise
    with open(configfilename(configbase), 'w') as configfile:
        json.dump(config, configfile, indent=4)
        configfile.write("\n")
    return

def resetconfig(configbase):
    """
    Reset configuration in indicated directory
    """
    dip_config = (
        { "dipbase":  None
        , "dipdir":   None
        })
    writeconfig(configbase, dip_config)
    return

def dip_show_config_item(config, itemname, prefix="", obscure=False):
    if (itemname in config) and (config[itemname] is not None):
        itemval = config[itemname]
        if obscure:
            itemval = "*"*len(itemval)
        print('''%s%s="%s"'''%(prefix, itemname, itemval))
    return

def dip_show_config(configbase, filebase):
    dip_config     = readconfig(configbase)
    dip_show_config_item(dip_config, "dipbase")
    dip_show_config_item(dip_config, "dipdir")
    if 'collections' in dip_config:
        for collection_uri in dip_config['collections']:
            coll_config = dip_config['collections'][collection_uri]
            dip_show_config_item(dip_config['collections'], "collection_uri")
            print('''collection_uri="%s"'''%(collection_uri))
            dip_show_config_item(coll_config, "servicedoc_uri", prefix="  ")
            dip_show_config_item(coll_config, "username", prefix="  ")
            dip_show_config_item(coll_config, "password", prefix="  ", obscure=True)
    return

def dip_get_default_dir(configbase):
    dip_config = readconfig(configbase)
    return dip_config['dipdir']

def dip_set_default_dir(configbase, filebase, dipdir, display=False):
    dip_config = readconfig(configbase)
    dip_config.update({'dipbase': filebase, 'dipdir': dipdir})
    writeconfig(configbase, dip_config)
    if display:
        dip_show_config_item(dip_config, "dipbase")
        dip_show_config_item(dip_config, "dipdir")
    return diperrors.DIP_SUCCESS

def dip_get_dip_dir(configbase, filebase, options, default=False):
    dip_config = readconfig(configbase)
    dipref     = strip_quotes(options.dip)
    if not dipref and default:
        dipref = dip_config['dipdir']
    if not dipref:
        print("No directory specified for DIP", file=sys.stderr)
        return (diperrors.DIP_NODIPGIVEN, None)
    dipdir = os.path.join(filebase, dipref)
    return (diperrors.DIP_SUCCESS, dipdir)

def dip_get_service_details(configbase, filebase, options, createnew=False):
    dip_config     = readconfig(configbase)
    collection_uri = strip_quotes(options.collection_uri)
    if not collection_uri:
        print("No SWORD collection specified for deposit", file=sys.stderr)
        return (diperrors.DIP_NOCOLLECTION, None)
    if  ( ('collections'  in dip_config) and 
          (collection_uri in dip_config['collections']) ):
        svcinfo = dip_config['collections'][collection_uri]
        # log.debug("svcinfo for %s: %r"%(collection_uri, dip_config['collections']))
        ss = SwordService(
            collection_uri=collection_uri,
            servicedoc_uri=strip_quotes(options.servicedoc_uri) or svcinfo.get('servicedoc_uri', None),
            username=strip_quotes(options.username) or svcinfo.get('username', None),
            password=strip_quotes(options.password) or svcinfo.get('password', None)
            )
    elif createnew:
        ss = SwordService(
            collection_uri=collection_uri,
            servicedoc_uri=None,
            username=None,
            password=None
            )
    else:
        print("Unknown SWORD collection specified for deposit (use dip config to configure)", file=sys.stderr)
        return (diperrors.DIP_UNKNOWNCOLL, None)
    return (diperrors.DIP_SUCCESS, ss)

def dip_save_service_details(configbase, filebase, ss, dip_config=None):
    collection_uri = ss.collection_uri
    if dip_config is None:
        dip_config = readconfig(configbase)
    if 'collections' not in dip_config:
        dip_config['collections'] = {}
    if collection_uri in dip_config['collections']:
        svcinfo = dip_config['collections'][collection_uri].copy()
    else:
        svcinfo = {}
    if ss.servicedoc_uri:
        svcinfo['servicedoc_uri'] = ss.servicedoc_uri
    if ss.username:
        svcinfo['username'] = ss.username
    if ss.password:
        svcinfo['password'] = ss.password
    dip_config['collections'][collection_uri] = svcinfo
    writeconfig(configbase, dip_config)
    return diperrors.DIP_SUCCESS

def dip_set_service_details(configbase, filebase, options):
    dip_config     = readconfig(configbase)
    collection_uri = strip_quotes(options.collection_uri)
    if not collection_uri:
        print("No SWORD collection specified", file=sys.stderr)
        return (diperrors.DIP_NOCOLLECTION, None)
    (status, ss) = dip_get_service_details(configbase, filebase, options, createnew=True)
    if status == diperrors.DIP_SUCCESS:
        status = dip_save_service_details(configbase, filebase, ss, dip_config=dip_config)
    if status == diperrors.DIP_SUCCESS:
        print('''collection_uri="%s"'''%(collection_uri))
        svcinfo = dip_config['collections'][collection_uri]
        dip_show_config_item(svcinfo, "servicedoc_uri")
        dip_show_config_item(svcinfo, "username")
        dip_show_config_item(svcinfo, "password", obscure=True)
    return status

# End.
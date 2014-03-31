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

CONFIGFILE = "dip_config.json"

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

def dip_get_default_dir(configbase):
    dip_config = readconfig(configbase)
    return dip_config['dipdir']

def dip_set_default_dir(configbase, dipdir):
    dip_config = readconfig(configbase)
    dip_config.update({'dipdir': dipdir})
    writeconfig(configbase, dip_config)
    return

def dip_get_dip_dir(configbase, filebase, options, default=False):
    dip_config = readconfig(configbase)
    dipref = options.dip
    if not dipref and default:
        dipref = dip_config['dipdir']
    if not dipref:
        print("No directory specieid for DIP", file=sys.stderr)
        return (2, None)
    dipdir = os.path.join(filebase, dipref)
    dip_config.update({'dipbase': filebase, 'dipdir': dipdir})
    writeconfig(configbase, dip_config)
    return (0, dipdir)

# End.
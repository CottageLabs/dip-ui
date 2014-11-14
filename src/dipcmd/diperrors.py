# !/usr/bin/env python
"""
diperrors.py - status codes returns by dipcmd
"""

from __future__ import print_function

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2013-2014, University of Oxford"
__license__     = "MIT (http://opensource.org/licenses/MIT)"


# Status return codes
DIP_SUCCESS         = 0     # Success
DIP_PENDING         = 1     # Operation pending
DIP_ATTRNOTFOUND    = 2     # Attribute not present
DIP_BADCMD          = 64    # Command error
DIP_EXISTS          = 65    # directory already exists
DIP_NOTEXISTS       = 66    # Directory does not exist
DIP_NODIPHERE       = 67    # Directory does not contain a deposit information package
DIP_NOFILES         = 68    # No files specified for add-files or add-metadta-files
DIP_NOATTRIBUTES    = 69    # No attributes specified for add/show/remove-attributes
DIP_INVALIDATTR     = 70    # Attribute name+value supplied is not a valid form
DIP_UNKNOWNATTR     = 71    # Unknown attribute name
DIP_NODIPGIVEN      = 72    # No DIP directory specified or available
DIP_NOCOLLECTION    = 73    # SWORD collection specified for deposit
DIP_UNKNOWNCOLL     = 74    # Unknown SWORD collection specified 
DIP_NOUSERNAME      = 75    # No username specified (command line or config?)
DIP_NOPASSWORD      = 76    # No password specified (command line or config?)

# !/usr/bin/env python
"""
diperrors.py - status codes returns by dipcmd
"""

from __future__ import print_function

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2013-2014, University of Oxford"
__license__     = "MIT (http://opensource.org/licenses/MIT)"


# Status return codes
DIP_SUCCESS     = 0     # Success
DIP_PENDING     = 1     # Operation pending
DIP_BADCMD      = 64    # Command error
DIP_EXISTS      = 65    # directory already exists
DIP_NOTEXISTS   = 66    # Directory does not exist
DIP_NODIPHERE   = 67    # Directory does not containa deposit information package
DIP_NOFILES     = 68    # No files specified for add-files or add-metadta-files

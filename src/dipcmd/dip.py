# !/usr/bin/env python
#
# dip.py - command line tool to create and submit deposit information packages
#

from __future__ import print_function

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2011-2013, University of Oxford"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import sys
import os
import os.path
import re
import argparse
import logging
import errno

log = logging.getLogger(__name__)

# Make sure MiscUtils can be found on path
# if __name__ == "__main__":
#     sys.path.append(os.path.join(sys.path[0],"../.."))


VERSION = "0.1"

def parseCommandArgs(argv):
    """
    Parse command line arguments

    argv            argument list from command line

    Returns a pair consisting of options specified as returned by
    OptionParser, and any remaining unparsed arguments.
    """
    # create a parser for the command line options
    parser = argparse.ArgumentParser(
                description="Create, manipulate or submit deposit information package",
                epilog=("\n"+
                    "On successful creation of a new DIP, its directory is written to standard output.\n"+
                    "On successful deposit of a DIP, its URI is written to standard output."
                    )
                )
    parser.add_argument("command", metavar="COMMAND",
                        nargs=None,
                        help="sub-command, which is one of: "+
                             "create, use, show, remove-dip, "+
                             "add-file, add-metadata, remove-file, "+
                             "package, deposit"
                       )
    parser.add_argument("files", metavar="FILES",
                        nargs="*",
                        help="Zero, one or more files that are added to a DIP "+
                             "(add-files and add-metadata sub-commands only)")
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)
    parser.add_argument("-d", "--dip",
                        dest="dip", metavar="DIP",
                        default=None,
                        help="Directory of DIP")
    parser.add_argument("-p", "--package",
                        dest="package", metavar="PACKAGE",
                        default=None,
                        help="Package for deposit (or other operation...)")
    parser.add_argument("-r", "--recursive",
                        action="store_true", 
                        dest="recursive", 
                        default=False,
                        help="Add or remove files recursively (i.e. scan subdirectories)")
    parser.add_argument("--debug",
                        action="store_true", 
                        dest="debug", 
                        default=False,
                        help="Run with full debug output enabled")
    # parse command line now
    options = parser.parse_args(argv)
    if options and options.command:
        return options
    print("No valid usage option given.", file=sys.stderr)
    parser.print_usage()
    return None

def run(configbase, filebase, options, progname):
    """
    Command line tool to create and submit deposit informationm packages
    """
    status = 0
    if options.command == "config":
        raise NotImplementedError("@@TODO config")
    if options.command == "create":
        raise NotImplementedError("@@TODO create")
    elif options.command == "use":
        raise NotImplementedError("@@TODO use")
    elif options.command == "show":
        raise NotImplementedError("@@TODO show")
    elif options.command == "remove":
        raise NotImplementedError("@@TODO remove")
    elif options.command == "add-file":
        raise NotImplementedError("@@TODO add-file")
    elif options.command == "add-metadata":
        raise NotImplementedError("@@TODO add-metadata")
    elif options.command in  ["remove-file", "remove-metadata"]:
        raise NotImplementedError("@@TODO remove-file")
    elif options.command == "package":
        raise NotImplementedError("@@TODO package")
    elif options.command == "deposit":
        raise NotImplementedError("@@TODO deposit")
    else:
        print("Un-recognised sub-command: %s"%(options.command), file=sys.stderr)
        print("Use '%s --help' to see usage summary"%(progname), file=sys.stderr)        
        status = 1
    # Exit
    return status

def runCommand(configbase, filebase, argv):
    """
    Run program with supplied configuration base directory, Base directory
    from which to start looking for research objects, and arguments.

    This is called by main function (below), and also by test suite routines.

    Returns exit status.
    """
    options = parseCommandArgs(argv[1:])
    if options and options.debug:
        logging.basicConfig(level=logging.DEBUG)
    log.debug("runCommand: configbase %s, filebase %s, argv %s"%(configbase, filebase, repr(argv)))
    log.debug("Options: %s"%(repr(options)))
    # else:
    #     logging.basicConfig()
    status = 1
    if options:
        progname = os.path.basename(argv[0])
        status   = run(configbase, filebase, options, progname)
    return status

def runMain():
    """
    Main program transfer function for setup.py console script
    """
    userhome = os.path.expanduser("~")
    filebase = os.getcwd()
    return runCommand(userhome, filebase, sys.argv)

if __name__ == "__main__":
    """
    Program invoked from the command line.
    """
    status = runMain()
    sys.exit(status)

    # End.


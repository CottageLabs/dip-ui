# dip-ui

Deposit information package user interfaces

# Command options

DIP = deposit information package.  A DIP contains *references* to files elsewhere in the local file system.

Example session (using default `--dip` values where possible):

    dip create --dip=~/workspace/dip/mypackage  
    dip show
    dip add-file --recursive ~/workspace/ros/myresearchobject
    dip add-metadata ~/workspace/ros/myresearchobject/metadata
    PACKAGE=$(dip package)
    dip deposit --package=$PACKAGE http://databank.bodeian.ox.ac/test-deposit/...?
    dip show

The `dip package` and `dip deposit` commands could (almost) equivalently be just:

    dip deposit

## dip config ...

Sets configuration options

Details TBD.

    user?
    dip directory?

## Create empty DIP

    dip create --dip=<directory>

Creates empty DIP, and establishes it as the default DIP for subsequent commands.

Error if directory already exists.

## Set default DIP

    dip use --dip=<directory>

Error if directory does not exist or is not recognisable as a DIP.

## Display a DIP

    dip show [--dip=<directory>]

Displays content of indicated DIP.

Error if directory does not exist or is not recognisable as a DIP.

## Delete a DIP

    dip remove --dip=<directory>

Removers a deposit information package, but does not remove files that have been added to it.

Error if directory does not exist or is not recognisable as a DIP.

Note: --dip does not default in this case

## Add file(s) to a DIP

    dip add-file [--recursive] [--dip=<directory>] file, ...

Adds specified files to a DIP.  Adds references to the files, and does not create copies or snapshots at this stage.

## Add metadata to a DIP

    dip add-metadata --format=<meta-format> [--recursive] [--dip=<directory>] file, ...

Adds specified metadata files to a DIP.

## Remove file(s) or metadata from a DIP 

    dip remove-file [--recursive] [--dip=<directory>] file, ...
    dip remove-metadata [--recursive] [--dip=<directory>] file, ...

Removes data or metadata from a DIP.

## Package DIP ready for deposit

    dip package [--dip=<directory>]

Takes snapshots of data/metadata as appropriate.

Returns name of package file on stdout.

## Deposit DIP to designated repository

    dip deposit [--dip=<directory> | --package=<file>] <repository-uri>

Returns URI of deposited package on stdout.



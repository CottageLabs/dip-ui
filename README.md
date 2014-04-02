# dip-ui

Deposit information package user interfaces


# Getting started

## Installation

    cd $BASEDIR
    git clone git@github.com:CottageLabs/dip-ui.git

@@TODO: provide proper setup.py; create virtalenv for installation; etc./

## Testing

Instructions assume starting with current directory being the root of the dip-ui project; e.g.

    $ pwd
    /Users/graham/workspace/github/cottagelabs/dip-ui

1. Create and activate python virtual environment:

        virtualenv dipenv
        . dipenv/bin/activate

2. Install lxml (used by `dip`, but not imnstalled as dependency):

        pip install lxml

3. Install `dip`.  I am assuming dip repository is in sibling directory of `dip-ui` project.

        cd ../dip/
        python setup.py build
        python setup.py install
        cd ../dip-ui

4. Install nose:

        pip install nose

5. Run tests:

        cd src
        nosetests


# Command options

DIP = deposit information package.  A DIP contains *references* to files elsewhere in the local file system.

Example session (using default `--dip` values where possible):

    dip create --dip=~/workspace/dip/mypackage  
    dip show
    dip add-file --recursive ~/workspace/ros/myresearchobject
    dip add-metadata ~/workspace/ros/myresearchobject/metadata
    PACKAGE=$(dip package)
    STATUS=$(dip deposit --package=$PACKAGE --endpoint=http://databank.bodeian.ox.ac/test-deposit/...?)
    DEPOSITED=$(dip status $STATUS)
    dip show

The `dip package` and `dip deposit` commands could (almost) equivalently be just:

    dip deposit


## dip config ...

Sets configuration options

Details TBD.

    user?
    dip directory?

The main purpose of this will probably be to establish parameters for sword collections.


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

Note: `--dip` does not default in this case


## Add file(s) to a DIP

    dip add-file [--recursive] [--dip=<directory>] file, ...

Adds specified files to a DIP.  Adds references to the files, and does not create copies or snapshots at this stage.

Error if DIP directory does not exist or is not recognisable as a DIP.


## Add metadata to a DIP

    dip add-metadata --format=<meta-format> [--recursive] [--dip=<directory>] file, ...

Adds specified metadata files to a DIP.

Error if DIP directory does not exist or is not recognisable as a DIP.


## Remove file(s) or metadata from a DIP 

    dip remove-file [--recursive] [--dip=<directory>] file, ...
    dip remove-metadata [--recursive] [--dip=<directory>] file, ...

Removes data or metadata from a DIP.

Error if DIP directory does not exist or is not recognisable as a DIP.


## Package DIP ready for deposit

    dip package [--dip=<directory>]

Takes snapshots of data/metadata as appropriate.

Returns name of package file on stdout.

Error if DIP directory does not exist or is not recognisable as a DIP.


## Deposit DIP to designated repository

    dip deposit [--dip=<directory> | --package=<file>] --endpoint=<collection-uri>

Returns a token that can be used withj `dip status` (below) to obtain progress information about the deposit.  The `--endpoint` option specofies a SWORD collection-URI (corresponding to a Databank silo), which is used as a primary key for accessing otrher information about the target server.  Additional information may be preconfigired (cf. `dip config`) or auto-discovered from the server or other catalogue.

Defaults to current DIP if neither `--dip` or `--package` are specified.

Error if DIP directory does not exist or is not recognisable as a DIP, or package file is not a previously created DIP submission package.


## Check status of deposit

    dip status [--dip=<directory> | --package=<file>] --token=<deposit-token>

Interrogates the status of a deposit identified by the supplied token (returned by a previous invocation of `dip deposit`).

Exit status:

* 0: deposit completed successfully.  Returns URI of deposited package on stdout.
* 1: deposit in progress, not completed.
* 64 or greater: deposit failed.

(cf. http://stackoverflow.com/questions/1101957/are-there-any-standard-exit-status-codes-in-linux)

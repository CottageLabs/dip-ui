# dip-ui

Deposit information package user interfaces


## Getting started

### Installation

    cd $BASEDIR
    virtualenv dipenv
    . dipenv/bin/activate
    git clone git@github.com:CottageLabs/dip.git
    cd dip
    python setup.py build
    python setup.py install
    cd ..
    git clone git@github.com:CottageLabs/dip-ui.git
    cd dip-ui/src
    python setup.py build
    python setup.py install
    cd ..

NOTE: On MacOS 10.9 (with XCode), when installing the `dip` package, the attempted installation of `lxml` fails with the following messages:

    Processing dependencies for dip==0.1
    Searching for lxml
    Reading http://pypi.python.org/simple/lxml/
    Best match: lxml 3.4.0
    Downloading https://pypi.python.org/packages/source/l/lxml/lxml-3.4.0.tar.gz#md5=bc90cc4e4ee04e1f8290ae0f70e34eea
    Processing lxml-3.4.0.tar.gz
    Running lxml-3.4.0/setup.py -q bdist_egg --dist-dir /var/folders/tw/z2lyyvzx1sq1qrvkp9qmgtb40000gn/T/easy_install-9ibfoR/lxml-3.4.0/egg-dist-tmp-wDDmW1
    Building lxml version 3.4.0.
    Building without Cython.
    Using build configuration of libxslt 1.1.28
    /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/distutils/dist.py:267: UserWarning: Unknown distribution option: 'bugtrack_url'
      warnings.warn(msg)
    In file included from src/lxml/lxml.etree.c:232:
    /var/folders/tw/z2lyyvzx1sq1qrvkp9qmgtb40000gn/T/easy_install-9ibfoR/lxml-3.4.0/src/lxml/includes/etree_defs.h:14:10: fatal error:
          'libxml/xmlversion.h' file not found
    #include "libxml/xmlversion.h"
             ^
    1 error generated.
    error: Setup script exited with error: command 'cc' failed with exit status 1

To fix this, I used the following command before running `setup.py install`:

    CPATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/libxml2 pip install lxml==2.3.4

(See http://stackoverflow.com/a/22333123/324122)


### Testing

Instructions assume starting with current directory being the root of the dip-ui project, but do not assume completion of the installation process above; e.g.

    $ pwd
    /Users/graham/workspace/github/cottagelabs/dip-ui

1. Create and activate python virtual environment:

        virtualenv dipenv
        . dipenv/bin/activate

2. Install lxml (used by `dip`, but not installed as dependency):

        pip install lxml

    or, if that fails (on MacOS 10.9):

        CPATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/libxml2 pip install lxml==2.3.4

    (See http://stackoverflow.com/a/22333123/324122)


3. Install `dip`.  I am assuming dip repository is in sibling directory of `dip-ui` project.

        cd ../dip/
        python setup.py build
        python setup.py install
        cd ../dip-ui

4. Install nose:

        pip install nose

5. Install Simple-Sword-Server.  See [Notes/installing-sss-for-testing.md](Notes/installing-sss-for-testing.md) for details.

6. Edit collection URI in `src/tests/test-dip-cmd.py`; e.g.:

        SSS = SwordService(
            collection_uri="http://localhost:8080/col-uri/02cbab10-c995-41c9-8ff5-8bebc225e082",
            servicedoc_uri="http://localhost:8080/sd-uri",
            username="sword",
            password="sword"
            )

    where the `collection_uri` value is one of the values obtained from an instance of `Simple-Sword-Server` running on the local machine by browsing to [http://localhost:8080/sd-uri]()), and then looking for an XML element of the form:

        <collection href="http://localhost:8080/col-uri/02cbab10-c995-41c9-8ff5-8bebc225e082">
            :
        </collection>

    The value of the `href=` attibute can be used as the value for `collection_uri` in `src/tests/test-dip-cmd.py`.

7. Run tests:

        cd src
        nosetests


## Command options

DIP = deposit information package.  A DIP contains *references* to files elsewhere in the local file system.

Example session (using default `--dip` values where possible):

    dip create --dip=~/workspace/dip/mypackage  
    dip show
    dip add-file --recursive ~/workspace/ros/myresearchobject
    dip add-metadata --format=text/json-ld ~/workspace/ros/myresearchobject/metadata
    PACKAGE=$(dip package)
    STATUS=$(dip deposit --package=$PACKAGE --endpoint=http://databank.bodeian.ox.ac/test-deposit/...?)
    DEPOSITED=$(dip status $STATUS)
    dip show

The `dip package` and `dip deposit` commands could (almost) equivalently be just:

    dip deposit


### dip config

Sets configuration options, which are stored localy in `~/.dip_ui/dip_config.json` (or equivalent per-user configuration file directory).

    dip config --collection_uri=<collection_uri> \
        [ --servicedoc_uri=<servicedoc_uri> ] \
        [ --username=<username> ] \
        [ --password=<password> ] \
        [ --dip=<dip_directory> ]

The main purpose of this is to establish default parameters for sword collections.

If `<dip_directory>` is given, it establishes a default directory for subserquent commands.

The `<collection_uri>` parameter is required, and specifies a collection for which access parameters are being defined.

If `<servicedoc_uri>` is given, if updates the service document for the Sword endpoint associated with the speciofied collection.

If `<username>` is given, it updates the user name used to access the specified collection.

If `<password>` is given, it updates the password used to access the specified collection.


### Create empty DIP

    dip create --dip=<directory>

Creates empty DIP, and establishes it as the default DIP for subsequent commands.

Error if directory already exists.


### Set default DIP

    dip use --dip=<directory>

Error if directory does not exist or is not recognisable as a DIP.


### Display a DIP

    dip show [--dip=<directory>]

Displays content of indicated DIP.

Error if directory does not exist or is not recognisable as a DIP.


### Delete a DIP

    dip remove --dip=<directory>

Removers a deposit information package, but does not remove files that have been added to it.

Error if directory does not exist or is not recognisable as a DIP.

Note: `--dip` does not default in this case


### Add file(s) to a DIP

    dip add-file [--recursive] [--dip=<directory>] file, ...

Adds specified files to a DIP.  Adds references to the files, and does not create copies or snapshots at this stage.

Error if DIP directory does not exist or is not recognisable as a DIP.


### Add Dublin Core metadata to a DIP

    dip add-attribute [--dip=<directory>] dc:<name>="<value>" ...

Adds or updates specified Dublin Core metadata attribute(s) to a package.  Quotes around `<value>` are optional if it does not contain spaces or other special characxters.

Allowable values for the attribute `<name>` are:

* `creator` (string) - name of creator
* `created` (timestamp) - date/time of creation
* `title` (string) - title of package
* `identifier` (string) - an identifier for the package

These are an initial set of supported metadata values.  In the longer term, we expect to support a wider range of values, and also a file-based mechanism for providing arbitrary additional metadata about a package and its contents.


### Remove Dublin Core metadata

    dip remove-attribute [--dip=<directory>] dc:<name> ...

Removes specified Dublin Core metadata attribute(s) from a package.

Allowable values for the attribute `<name>` are the same as for `add-attribute`.

Exit status `2` if a named attribute is not defined.


### Show Dublin Core metadata

    dip show-attribute [--dip=<directory>] dc:<name> ...

Shows specified Dublin Core metadata attribute(s) in a package.  Attribute values are written to standard output, one per line, in the format:

    dc:<name>="value"

This is the same format that can be used on the command line when defining an attribute.

Exit status `2` if a named attribute is not defined.

Allowable values for the attribute `<name>` are the same as for `add-attribute`.


### Add metadata to a DIP

    dip add-metadata --format=<meta-format> [--recursive] [--dip=<directory>] file, ...

Adds specified metadata files to a DIP.

Error if metadata format is not recognized, or data provided doesn't confirm to indicated format.

Error if DIP directory does not exist or is not recognisable as a DIP.

@@TODO: need to clarify `<meta-format>` options.

@@TODO: Not yet implemneted in `dip`


### Remove file(s) or metadata from a DIP 

    dip remove-file [--recursive] [--dip=<directory>] file ...
    dip remove-metadata [--recursive] [--dip=<directory>] file ...

Removes data or metadata from a DIP.

Error if DIP directory does not exist or is not recognisable as a DIP.


### Package DIP ready for deposit

    dip package [--dip=<directory>]

Takes snapshots of data/metadata as appropriate.

Returns name of package file on stdout.

Error if DIP directory does not exist or is not recognisable as a DIP.


### Deposit DIP to designated repository

    dip deposit [--dip=<directory> | --package=<file>] --collection=<collection-uri>

Returns a token that can be used withj `dip status` (below) to obtain progress information about the deposit.  The `--collection` option specifies a SWORD collection-URI (corresponding to a Databank silo), which is used as a primary key for accessing other information about the target server.  Additional information may be preconfigured (cf. `dip config`) or auto-discovered from the server or other catalogue.

Defaults to current DIP if neither `--dip` or `--package` are specified.

Displays a deposit token on sdout, in the form:

    token=<deposit-token>

Error if DIP directory does not exist or is not recognisable as a DIP, or package file is not a previously created DIP submission package.


### Check status of deposit

    dip status [--dip=<directory> | --package=<file>] --token=<deposit-token>

Interrogates the status of a deposit identified by the supplied token (returned by a previous invocation of `dip deposit`).

Exit status:

* 0: deposit completed successfully.  Returns URI of deposited package on stdout.
* 1: deposit in progress, not completed.
* 64 or greater: deposit failed.

(cf. http://stackoverflow.com/questions/1101957/are-there-any-standard-exit-status-codes-in-linux)

@@TODO: the current deposit implementation is synchronous, so exit status 1 is not used.  


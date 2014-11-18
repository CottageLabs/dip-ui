# Installing Simple-Sword-Server form dip-ui testing

Some of the `dip-ui` tests assumes that `SSS`, or `Simple-Sword-Server`, (from [here](https://github.com/swordapp/Simple-Sword-Server)) is running on port 8080.

I ran into all sorts of problems getting SSS to run cleanly for testing.

# Installing lxml (on MacOS)

One problem was that I couldn't get the required version of lxml installed; eventually I tried this:

    CPATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/libxml2 pip install lxml==2.3.4

and it seemed to work.  (See http://stackoverflow.com/a/22333123/324122)

# Installing Simple-Sword-Server

With `Simple-Sword-Server` source code project cloned from github:

    . *pyenv*/bin/activate
    python setup.py build
    python setup.py install

(where `*pyenv*` is the Python virtual environment used to run SSS)

# Running Simple-Sword-Server

The obvious command would be:

    python sss/sss-1.0.py

and at first this appears to work.  But then it throws a "500 Server Error" when trying to access it, logging a module import error.

The problem appears to be that `sss-1.0` is not a valid Python mopdule name.  So:

    ln -s sss-1.0.py sss.py
    python sss.py

and all seems well.

Note that, for testing, `SSS` can be installed in the same virtualenv as `dip` and `dip-ui`, or may be run in a separate environment.

# Configure `dip-ui` tests to use SSS collection

We need to use a valid collection URI in the dip-ui test suite.  Browse to [http://localhost:8080/]() or to obtain a list of collection identifiers.

The service document is also shown at [http://localhost:8080/sd-uri]() - to view this, default credentials are `sword` and `sword`.  The service document contains links to full collection URIs which are used by the SWORD client.

The `dip-ui` test suite configuration (in `src/tests/test_dip_cmp.py`) may need adjusting to use this:  the relevant block of code is about line 44:

    SSS = SwordService(
        collection_uri="http://localhost:8080/col-uri/02cbab10-c995-41c9-8ff5-8bebc225e082",
        servicedoc_uri="http://localhost:8080/sd-uri",
        username="sword",
        password="sword"
        )

Just the `collection_uri` value needs to be adjusted;  the other values here correspond to SSS installation default values.


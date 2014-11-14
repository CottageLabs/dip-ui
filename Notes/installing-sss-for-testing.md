# Installing Simple-Sword-Server form dip-ui testing

One of the `dip-ui` tests assumes that `SSS`, or `Simple-Sword-Server`, (from [here](https://github.com/swordapp/Simple-Sword-Server)) is running on port 8000.

I ran into all sorts of problems getting SSS to run cleanly for testing.

# Installing lxml (on MacOS)

One problem was that I couldn't get the required version of lxml installed; eventually I tried this:

    CPATH=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/libxml2 pip install lxml==2.3.4

and it seemed to work.

# Installing Simple-Sword-Server

With `Simple-Sword-Server` source code project cloned from github:

    *pyenv*/bin/activate
    python setup.py build
    python setup.py install

(where *pyenv* is the Python virtual environment used to run SSS)

# Running Simple-Sword-Server

The obvious commnand would be:

    python sss/sss-1.0.py

and at first this appears to work.  But thenj it throws a "500 Server Error" when trying to accdess it, logging a module import error.

The problem appears to be that `sss-1.0` is not a vali8d Python mopdule name.  So:

    ln -s sss-1.0.py sss.py
    python sss.py

and all seems well.

Next, we need to use a valid collection URI in the dip-ui test suite.  Browse to [http://localhost:8080/]() to obtrain a list of collection URIs.

The service document isd also shown - to view this, default credentials are `sword` and `sword`.

The service document contains links to collection URIs which are used by thw SWORD client.

The `dip-ui` test suite configuration (in `test_dip_cmp.py` may need tweaking for this.)

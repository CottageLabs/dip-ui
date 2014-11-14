# dip-ui TODO

- [x] Obtain servicedoc from config if not given - this is working in test_42_dip_deposit_sss (is part of stored collection metadata)
- [x] Define message values for DIP_NOUSERNAME and DIP_NOPASSWORD
- [ ] Servicedoc discovery if not given?
- [ ] Obtain collection_uri from config?
- [x] Figure out token response from deposit?  Currently using deposit receipt id for token.

## Commands

    python dipmain.py create --dip=/tmp/diptest
    python dipmain.py show
    python dipmain.py --recursive add-file ../tests/test/data/files/
    python dipmain.py show
    python dipmain.py package
    python dipmain.py config 
        --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e 
        --servicedoc_uri=http://localhost:8080/sd-uri 
        --username=sword 
        --password=sword
    python dipmain.py deposit 
        --package=/tmp/diptest/packages/aHR0cDovL3B1cmwub3JnL25ldC9zd29yZC9wYWNrYWdlL1NpbXBsZVppcA==/SimpleZip.zip 
        --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e


## Manual deposit status

    (dipenv)oerc-dynamic-192:dipcmd graham$ python dipmain.py deposit --package=/tmp/diptest/packages/aHR0cDovL3B1cmwub3JnL25ldC9zd29yZC9wYWNrYWdlL1NpbXBsZVppcA==/SimpleZip.zip --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e
    Traceback (most recent call last):
      File "dipmain.py", line 290, in <module>
        status = runMain()
      File "dipmain.py", line 282, in runMain
        return runCommand(userhome, filebase, sys.argv)
      File "dipmain.py", line 271, in runCommand
        status   = run(configbase, filebase, options, progname)
      File "dipmain.py", line 240, in run
        basedir=os.getcwd()
      File "/usr/workspace/github/cottagelabs/dip-ui/src/dipcmd/dipdeposit.py", line 53, in dip_deposit
        raise ValueError("@@TODO - service document discovery")
    ValueError: @@TODO - service document discovery
    (dipenv)oerc-dynamic-192:dipcmd graham$

But:

    (dipenv)oerc-dynamic-192:dipcmd graham$ python dipmain.py deposit --package=/tmp/diptest/packages/aHR0cDovL3B1cmwub3JnL25ldC9zd29yZC9wYWNrYWdlL1NpbXBsZVppcA==/SimpleZip.zip --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e --servicedoc_uri=http://localhost:8080/sd-uri --username=sword --password=sword
    init None 2014-11-14 15:32:09.950947
    2014-11-14 15:32:09,954 - sword2.connection - INFO - keep_history=True--> This instance will keep a JSON-compatible transaction log of all (SWORD/APP) activities in 'self.history'
    2014-11-14 15:32:09,955 - sword2.connection - INFO - Adding username/password credentials for the client to use.
    2014-11-14 15:32:09,984 - sword2.connection - INFO - Received a Resource Created (201) response.
    2014-11-14 15:32:09,985 - sword2.connection - INFO - Server response included a Deposit Receipt. Caching a copy in .resources['http://localhost:8080/edit-uri/04a89ccb-afde-4198-a033-0be960c24b5e/5e3f2b18-b37f-4de5-b211-42e845147cf6']
    init 2014-11-14 15:32:09.950947 2014-11-14 15:32:09.950947




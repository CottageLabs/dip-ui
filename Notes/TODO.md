# dip-ui TODO

- [x] Obtain servicedoc from config if not given - this is working in test_42_dip_deposit_sss (is part of stored collection metadata)
- [x] Define message values for DIP_NOUSERNAME and DIP_NOPASSWORD
- [x] Servicedoc discovery if not given? (from config, for --package) (WORKING)
- [x] Obtain collection_uri from config. (WONTDO: config can contain sevral collection_uri values; need to say which one to use)
- [x] Deposit from supplied package file? (Test added)
- [x] Figure out token response from deposit?  Currently using deposit receipt id for token.
- [x] implement config command (DONE)
- [x] Metadata? (Attribute tests present; generic metadata out of scope for the current development)
- [ ] setup.py
- [ ] How to query status of previous deposit - need to save details locally, or can use SSS? 
- [ ] Test against Databank


## Commands for manual testing

    python dipmain.py create --dip=/tmp/diptest
    python dipmain.py show
    python dipmain.py --recursive add-file ../tests/test/data/files/
    python dipmain.py show
    python dipmain.py package
    python dipmain.py config \
        --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e \
        --servicedoc_uri=http://localhost:8080/sd-uri \
        --username=sword \
        --password=sword
    python dipmain.py deposit --dip=/tmp/diptest \
        --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e \
    python dipmain.py deposit
        --package=/tmp/diptest/packages/aHR0cDovL3B1cmwub3JnL25ldC9zd29yZC9wYWNrYWdlL1NpbXBsZVppcA==/SimpleZip.zip 
        --collection_uri=http://localhost:8080/col-uri/04a89ccb-afde-4198-a033-0be960c24b5e




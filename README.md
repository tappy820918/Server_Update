# Server_Update
Python Implemented Server Update system

## This Update.py file program is mainly to :
1. Set up connection from client to server via http
2. Download and start the running background program __mainfile__ 
3. Download setting file __setting__ for __mainfile__
4. Update __mainfile__ & __setting__ if the version is higher in Server/config.csv
- Note that in __mainfile__ all command **MUST NOT EXECUTE in IMPORTING**
    ( in the `check_output_cmd` we import __version__ from __mainfile__ )
- The version setting is controled by `StrictVersion` so should be set carefully
---

### First set the folder *Server* to same directory as Update.py
Run code:
 - On server side Terminal
```cmd
$ python -m SimpleHTTPServer 8000
```

 - On client side terminal
```
$ python Update.py
```

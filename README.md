# Server-Client update system

## File written in Python 2.7

## File structure (Initially)

- Server side: 3 files
  - **config.csv** - The configuration file which stores the version from Server side.
  - **Toy_setting.csv** - The setting file which will be set as parameter updating for __mailfile__.
  - **Toy.py** - The main file in which we want to run and updates.
- Client side: 1 file
  - **Update.py**

---

## Run code

On server side Terminal we change to the desired directory then initiate Server :

``` cmd
cd /desktop/
python -m SimpleHTTPServer 8000
```

On client side Terminal:

``` cmd
cd home/ubuntu/CL_update
python Update.py
```

---

## This update file program is mainly to

1. Set up connection from client to server via http.
1. Download and start the running background program__mainfile__ .
1. Download setting file __setting__ for __mainfile__ .
1. Update __mainfile__ & __setting__ if the version is higher in  **Server**/`config.csv` and `config.csv` & `file`'s version matches.

---

- Note that in __mainfile__ commands **MUST NOT EXECUTE in IMPORTING**; i.e. set`if __name__ == '__main__'` on the execution scripts.  ( In the `check_output_cmd` we import __version__ from __mainfile__ )
- Version setting is controled by `StrictVersion` soshould be set carefully in furthur __mainfile__setting

---

## Initial Setting for **Update.py**

> MAC = '10.137.99.226' - mac address  
>PORT = '8000' - port setting  
>__configuration__ = 'config.csv'  
>__mainfile__ = 'Toy.py'  
>__setting__ = 'Toy_setting.csv'  

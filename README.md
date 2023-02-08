# burp2httpx
```
               🦋
  🦋burp2httpx🦋
 🦋
```
Parse burpsuite request to python3 code

## Usage:

Copy the request you want to reproduce from Burpsuite and paste it in a text file.

Run burp2py.py giving the path to the text file as argument. -o saves the output in a file.

The script will generate an [httpx](https://github.com/encode/httpx) Client() with the data provided.

``` bash
python3 burp2py.py burpreq.txt -o req.py
```

# Time-Based Blind tool
Piccolo tool per effettuare attacchi su mysql sia con richieste GET che POST.

### Prerequisiti

Per funzionare il tool necessita di python 2. Attenzione non funzionerà con python 3.

```
Python 2.7
```

## Librerie Utilizzate

```
import requests
import time
import sys
import binascii
import urlparse
```

### Sintassi

Per avviare il tool bisognerà digitare da riga di comando i seguenti parametri

```
python2.7 daje.py url metodo 'parametri'
```

Per esempio

```
python2.7 daje.py http://192.168.33.10/sqli/time_based_blind.php GET 'email=arthur@guide.com'
python2.7 daje.py http://vip.hacking.w3challs.com/index.php?page=contact POST 'destin=1&&msg=1'
```


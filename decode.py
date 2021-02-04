#!/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import requests
import json
import base64

r = requests.get("http://127.0.0.1:8500/v1/kv/ledivan/ledivan/chave")
d = str(json.loads(r.text)[0]["Value"])
print(base64.b64decode(d).decode("ascii"))
### TypeError: list indices must be integers or slices, not str
########

encoded = 'YmFzZTY0IGVuY29kZWQgc3RyaW5n'
data = base64.b64decode(encoded)
print(data.decode("ascii"))

##################################

#!/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import requests
import json
import  pprint

headers={"X-Vault-Token": "XXXXXXX"}

response = requests.get("http://127.0.0.1:8200/v1/secret/data/ledivan-teste",headers=headers)

print(json.loads(response.text)["data"]["data"]["ledivan"])


### curl  -H "X-Vault-Token: XXXXXXXX" -X GET http://127.0.0.1:8200/v1/secret/data/ledivan-teste |  python3 -c 'import sys, json; print (json.load(sys.stdin)["data"]["data"]["ledivan"])'

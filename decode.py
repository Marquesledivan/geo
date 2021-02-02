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

########

encoded = 'YmFzZTY0IGVuY29kZWQgc3RyaW5n'
data = base64.b64decode(encoded)
print(data.decode("ascii"))

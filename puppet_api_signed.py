#!/usr/local/bin/python3
# https://puppet.com/docs/pe/2019.8/classification_endpoint_v2.html
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""

import requests
import pprint
import json
import getpass
import os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

jobs = []

def login_api():
     user = input("User:")
     passwd = getpass.getpass("Password: ")
     lifetime = "10h"
     data = {"login": user,"password": passwd, "lifetime": lifetime,"label": "four-hour token"}
     payload = json.dumps(data)
     headers={'Content-type': 'application/json'}
     r = requests.post("https://10.0.0.10:4433/rbac-api/v1/auth/token",verify=False,data=payload,headers=headers)
     token = r.json()["token"]
     with open("token.txt", "w") as f:
         f.write(token)
         f.close()
     with open("token.txt", "r") as f:
         return f.read()
         f.close()

def check_token():
    try:
        with open("token.txt", "r") as f:
            token = f.read()
            f.close()
        headers={'Content-type': 'application/json', 'X-Authentication': token}
        uri = requests.get("https://10.0.0.10:4433/rbac-api/v1/users/current",headers=headers,verify=False)
        if uri.status_code != 200:
            token = login_api()
    except FileNotFoundError as e:
        token = login_api()
    return token

lista = []
def pre_task():
     token = check_token()
     headers={'Content-type': 'application/json', 'X-Authentication': token}
     r = requests.get(f"http://10.0.0.10:8080/pdb/query/v4/nodes",headers=headers,verify=False)
     for i in json.loads(r.text):
          nodes = i["certname"]
          if nodes.startswith("local"):
              lista.append(nodes)

def run_task(nodes):
     token = check_token()
     headers={'Content-type': 'application/json', 'X-Authentication': token}
     r = requests.post(f"https://10.0.0.10:4433/classifier-api/v2/classified/nodes/{nodes}",headers=headers,verify=False)
     print("################################## Verificando o node:",nodes, "####################################")
     for i in json.loads(r.text)["classes"]:
          print(i)

if __name__ == "__main__":
    pre_task()
    for i in lista:
        run_task(i)

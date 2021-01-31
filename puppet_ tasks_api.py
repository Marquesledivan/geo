#!/usr/local/bin/python3
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

def login_api():
     user = input("Digite seu user:")
     passwd = getpass.getpass("Digite sua senha: ")
     data = {"login": user,"password": passwd, "lifetime": "4h","label": "four-hour token"}
     payload = json.dumps(data)
     headers={'Content-type': 'application/json'}
     r = requests.post("https://master.ledivan.com.br:4433/rbac-api/v1/auth/token",verify=False,data=payload,headers=headers)
     token = r.json()["token"]
     f = open("token.txt", "w")
     f.write(token)
     f = open("token.txt", "r")
     return f.read()


def check_token():
    try:
        f = open("token.txt", "r")
        token = f.read()
        headers={'Content-type': 'application/json', 'X-Authentication': token}
        uri = requests.get("https://master.ledivan.com.br:4433/rbac-api/v1/users/current",headers=headers,verify=False)
        if uri.status_code != 200:
            token = login_api()
    except FileNotFoundError as e:
        token = login_api()
    return token

def run_task(command,nodes):
     token = check_token()
     headers={'Content-type': 'application/json', 'X-Authentication': token}
     data = {"task":"bolt_shim::command","params":{"command": command },"scope":{"nodes":[nodes]}}
     payload = json.dumps(data)
     r = requests.post("https://master.ledivan.com.br:8143/orchestrator/v1/command/task",headers=headers,data=payload,verify=False)
     print(json.loads(r.text)["job"]["id"])

if __name__ == "__main__":
    run_task("ls -lha", "master.ledivan.com.br")

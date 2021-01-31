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

jobs = []

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
     jobs.append(json.loads(r.text)["job"]["name"])


def orchestrator_jobs(jobs):
     token = check_token()
     headers={'Content-type': 'application/json', 'X-Authentication': token}
     r = requests.get(f'https://master.ledivan.com.br:8143/orchestrator/v1/jobs/{jobs}?limit=20&offset=20',headers=headers,verify=False)
     i = json.loads(r.text)
     print(i["options"]["scope"]["nodes"],i["state"])


if __name__ == "__main__":
    f = open("hosts.txt", "r")
    hosts = f.read()
    for i in hosts.splitlines():
        run_task("ls -lha", i)
    for i in jobs:
        orchestrator_jobs(i)

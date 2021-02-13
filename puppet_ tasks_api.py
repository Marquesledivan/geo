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
     user = input("User:")
     passwd = getpass.getpass("Password: ")
     lifetime = "10m"
     data = {"login": user,"password": passwd, "lifetime": lifetime,"label": "four-hour token"}
     payload = json.dumps(data)
     headers={'Content-type': 'application/json'}
     r = requests.post("https://master.ledivan.com.br:4433/rbac-api/v1/auth/token",verify=False,data=payload,headers=headers)
     token = r.json()["token"]
     with open("token.txt", "w") as f:
         f.write(token)
         f.close()
 
def check_token():
    try:
        with open("token.txt", "r") as f:
            token = f.read()
            f.close()
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

def connect_status(nodes):
     token = check_token()
     headers={'Content-type': 'application/json', 'X-Authentication': token}
     r = requests.get(f'https://master.ledivan.com.br:8143/orchestrator/v1/inventory/{nodes}',headers=headers,verify=False)
     if json.loads(r.text)["connected"] == True:
         return True
     elif json.loads(r.text)["connected"] == False:
         return False

def stdout_jobs(jobs):
     token = check_token()
     headers={'Content-type': 'application/json', 'X-Authentication': token}
     r = requests.get(f'https://master.ledivan.com.br:8143/orchestrator/v1/jobs/{jobs}/nodes',headers=headers,verify=False)
     for i in json.loads(r.text)["items"]:
         print("Hostname:", i["name"], "Stdout:\n", i["result"]["stdout"])

if __name__ == "__main__":
    with open("hosts.txt", "r") as f:
        hosts = f.read()
        f.close()
    for i in hosts.splitlines():
        status = connect_status(i)
        if status == True:
            run_task("ls -lha", i)
        elif status == False:
            print("Host desconectado PXP:", i)
    for i in jobs:
        orchestrator_jobs(i)
    for i in jobs:
        stdout_jobs(i)

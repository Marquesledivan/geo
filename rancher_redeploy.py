#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""

import requests
import json
import os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

login_token = os.environ["token_api"]
rancher_url = "https://rancher.my.org"
username =  os.environ["username"]
password = os.environ["password"]

def login_user():
        token = {}
        headers = {'content-type': 'application/json',}
        params = (('action', 'login'),)
        data = {"username":username,"password":password}
        payload = json.dumps(data)
        response = requests.post(f'{rancher_url}/v3-public/localProviders/local', headers=headers, params=params, data=payload, verify=False)
        if response.status_code == 201:
            token["token"] = response.json()["token"]
            token["name"] = response.json()["name"]
            return token
        else:
             print("Error login api")

def login():
        token = {}
        description = "Deploy"
        cookies={'R_SESS': login_token}
        headers={'x-api-no-challenge': 'true','accept': 'application/json','x-api-action-links': 'actionLinks','content-type': 'application/json'}
        data = {"type":"token","description":description}
        payload = json.dumps(data)
        response = requests.post(f'{rancher_url}/v3/token', headers=headers, cookies=cookies, data=payload, verify=False)
        if response.status_code == 201:
            token["token"] = response.json()["token"]
            token["name"]  = response.json()["name"]
            return token
        else:
             print("Error login api")

token = login()
lista = []
ids = []

def list_wkl():
        token_api = token["token"]
        cookies={'R_SESS': token_api}
        headers={'Connection': 'keep-alive','x-api-no-challenge': 'true','accept': 'application/json','content-type': 'application/json'}
        params=(('limit', '-1'),('sort', 'name'))
        response = requests.get(f'{rancher_url}/v3/project/local:p-bvgkc/workloads', headers=headers, params=params, cookies=cookies, verify=False)
        if response.status_code == 200:
            for i in response.json()["data"]:
                lista.append(i["actions"]["redeploy"])
                ids.append(i["id"])
        else:
            print("Erro list Workloads")

def redeploy(url,ids):
        token_api = token["token"]
        cookies={'R_SESS': token_api}
        headers={'Connection': 'keep-alive','Accept': 'application/json','X-Requested-With': 'XMLHttpRequest'}
        params=(('action', 'redeploy'),)
        response = requests.post(url, headers=headers, params=params, cookies=cookies, verify=False)
        if response.status_code == 200:
                print('Redeploy Sucesso Workload:', ids)
        else:
                print("Redeploy Falha Workload:", ids)

def delete_token():
        name = token["name"]
        cookies = {'R_SESS': login_token}
        headers={'Connection': 'keep-alive','x-api-no-challenge': 'true','accept': 'application/json','x-api-action-links': 'actionLinks'}
        response = requests.delete(f'{rancher_url}/v3/tokens/{name}', headers=headers, cookies=cookies, verify=False)
        if response.status_code == 204:
                print("Delete Sucesso!!")
        else:
                print('Delete Falha!!')

if __name__ == "__main__":
        list_wkl()
        for url, wkl in zip(lista, ids):
                redeploy(url,wkl)
        delete_token()

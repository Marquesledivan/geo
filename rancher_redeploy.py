
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""

import requests
import pprint
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def login():
        token = {}
        headers = {'content-type': 'application/json',}
        params = (('action', 'login'),)
        data = '{"username":"","password":""}'
        response = requests.post('https://rancher.my.org/v3-public/localProviders/local', headers=headers, params=params, data=data, verify=False)
        token["token"] = response.json()["token"]
        token["name"] = response.json()["name"]
        return token

login_token = ""
token = login()
token_api = token["token"]
name = token["name"]

lista = []
ids = []
def list_wkl():
        cookies = {
                'R_SESS': token_api,
        }
        headers = {
                'Connection': 'keep-alive',
                'x-api-no-challenge': 'true',
                'accept': 'application/json',
                'content-type': 'application/json',
        }
        params = (
                ('limit', '-1'),
                ('sort', 'name'),
        )
        response = requests.get('https://172.16.16.101/v3/project/local:p-btsvc/workloads', headers=headers, params=params, cookies=cookies, verify=False)
        for i in response.json()["data"]:
                 lista.append(i["actions"]["redeploy"])
                 ids.append(i["id"])

list_wkl()

def redeploy(url,ids):
        cookies = {
                'R_SESS': token_api,
        }
        headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
        }
        params = (
                ('action', 'redeploy'),
        )
        response = requests.post(url, headers=headers, params=params, cookies=cookies, verify=False)
        if response.status_code == 200:
                print('Redeploy Sucesso Workload:', ids)
        else:
                print("Redeploy Falha Workload:", ids)

def delete_token():
        cookies = {
                'R_SESS': login_token,
        }

        headers = {
                'Connection': 'keep-alive',
                'x-api-no-challenge': 'true',
                'accept': 'application/json',
                'x-api-action-links': 'actionLinks',
        }

        response = requests.delete(f'https://172.16.16.101/v3/tokens/{name}', headers=headers, cookies=cookies, verify=False)
        if response.status_code == 204:
                print("Delete Sucesso!!")
        else:
                print('Delete Falha!!')


if __name__ == "__main__":
        for i, d in zip(lista, ids):
                redeploy(i,d)
        delete_token()

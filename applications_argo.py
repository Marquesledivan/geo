import requests
import json
import pprint
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

url = "https://localhost:8080"
app_name = "nginx"
def login():
    data = {"username":"admin","password":"admin"}
    payload = json.dumps(data)
    response = requests.post(f'{url}/api/v1/session',verify=False,data=payload)
    return response.json()["token"]

ARGOCD_TOKEN = login()

def list_repo():
    cookies = { 'argocd.token': f"{ARGOCD_TOKEN}" }
    response = requests.get(f'{url}/api/v1/repositories',verify=False,cookies=cookies)
    for i in response.json()["items"]:
        print(i["repo"])

def create_repo():
    cookies = { 'argocd.token': f"{ARGOCD_TOKEN}" }
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = '{"type":"git","name":"ledivan","repo":"git@github.com:Marquesledivan/nginx_k8s.git","sshPrivateKey":" ","insecure":true,"enableLfs":true}'
    response = requests.post('https://127.0.0.1:8080/api/v1/repositories', headers=headers, cookies=cookies, data=data, verify=False)
    print(response.status_code)


def delete():
    cookies = { 'argocd.token': f"{ARGOCD_TOKEN}" }
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    params = (
        ('cascade', 'true'),
        ('propagationPolicy', 'foreground'),
    )
    data = '{}'
    response = requests.delete('https://127.0.0.1:8080/api/v1/applications/nginx', headers=headers, params=params, cookies=cookies, data=data, verify=False)
    print(response.status_code)



def applications():
    cookies = { 'argocd.token': f"{ARGOCD_TOKEN}" }
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = {
    "metadata": {
        "name": app_name,
        "namespace": "argocd",
        "generation": 1,
        "managedFields": [
        {
            "manager": "argocd-server",
            "operation": "Update",
            "apiVersion": "argoproj.io/v1alpha1",
            "time": "2021-07-11T00:59:03Z",
            "fieldsType": "FieldsV1",
        }
        ]
    },
    "spec": {
        "source": {
        "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
        "path": "ledivan-app",
        "targetRevision": "HEAD"
        },
        "destination": {
        "server": "https://kubernetes.default.svc",
        "namespace": "teste"
        },
        "project": "default",
        "syncPolicy": {
        "automated": {
            "prune": True,
            "selfHeal": True
        },
        "syncOptions": [
            "Validate=false",
            "ApplyOutOfSyncOnly=true",
            "CreateNamespace=true"
        ]
        }
    },
    }
    payload = json.dumps(data)
    response = requests.post('https://127.0.0.1:8080/api/v1/applications', headers=headers, cookies=cookies, data=payload, verify=False)
    print(response.json())

applications()

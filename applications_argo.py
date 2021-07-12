# kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
# argocd app create ledivan-helm --repo git@github.com:Marquesledivan/nginx_k8s.git --path ledivan-app --dest-namespace ledivan --dest-server https://kubernetes.default.svc --helm-set replicaCount=2
# argocd app sync ledivan-helm
# argocd repo add git@github.com:Marquesledivan/nginx_k8s.git --insecure-ignore-host-key --ssh-private-key-path ~/.ssh/id_rsa
# https://argoproj.github.io/argo-cd/getting_started/
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

def sync():
    cookies = { 'argocd.token': f"{ARGOCD_TOKEN}" }
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://127.0.0.1:8080',
    }
    data = {
    "revision":"HEAD",
    "prune":False,
    "dryRun":False,
    "strategy":{"hook":{"force":False}},
    "syncOptions":{"items":["Validate': 'false",
    "ApplyOutOfSyncOnly=true",
    "CreateNamespace=true"]}
    }
    payload = json.dumps(data)
    response = requests.post('https://127.0.0.1:8080/api/v1/applications/nginx/sync', headers=headers, cookies=cookies, data=payload, verify=False)
    print(response.status_code)
    
    
def set_image():
    cookies = { 'argocd.token': f"{ARGOCD_TOKEN}" }

    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',

    }

    data ={
    "metadata": {
        "name": "nginx",
        "namespace": "argocd",
        "resourceVersion": "6390",
        "generation": 58,
        "managedFields": [
        {
            "manager": "argocd-server",
            "operation": "Update",
            "apiVersion": "argoproj.io/v1alpha1",
            "time": "2021-07-11T21:33:06Z",
            "fieldsType": "FieldsV1",
        },
        {
            "manager": "argocd-application-controller",
            "operation": "Update",
            "apiVersion": "argoproj.io/v1alpha1",
            "fieldsType": "FieldsV1",
        }
        ]
    },
    "spec": {
        "source": {
        "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
        "path": "ledivan-app",
        "targetRevision": "HEAD",
        "helm": {
            "parameters": [
            {
                "name": "image.tag",
                "value": "1.20.0"
            }
            ]
        }
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
    "status": {
        "resources": [
        {
            "version": "v1",
            "kind": "Service",
            "namespace": "teste",
            "name": "nginx-ledivan-app",
            "status": "Synced",
            "health": {
            "status": "Healthy"
            }
        },
        {
            "version": "v1",
            "kind": "ServiceAccount",
            "namespace": "teste",
            "name": "nginx",
            "status": "Synced"
        },
        {
            "group": "apps",
            "version": "v1",
            "kind": "Deployment",
            "namespace": "teste",
            "name": "nginx-ledivan-app",
            "status": "Synced",
            "health": {
            "status": "Healthy"
            }
        }
        ],
        "sync": {
        "status": "Synced",
        "comparedTo": {
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD",
            "helm": {
                "parameters": [
                {
                    "name": "image.tag",
                    "value": "1.20.0"
                }
                ]
            }
            },
            "destination": {
            "server": "https://kubernetes.default.svc",
            "namespace": "teste"
            }
        },
        "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c"
        },
        "health": {
        "status": "Healthy"
        },
        "history": [
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:14:35Z",
            "id": 0,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:14:26Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:15:35Z",
            "id": 1,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:15:34Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:18:06Z",
            "id": 2,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:18:06Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:20:44Z",
            "id": 3,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:20:44Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:28:21Z",
            "id": 4,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:28:21Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:28:36Z",
            "id": 5,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:28:35Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:29:13Z",
            "id": 6,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD"
            },
            "deployStartedAt": "2021-07-11T21:29:12Z"
        },
        {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "deployedAt": "2021-07-11T21:33:15Z",
            "id": 7,
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD",
            "helm": {
                "parameters": [
                {
                    "name": "image.tag",
                    "value": "1.20.0"
                }
                ]
            }
            },
            "deployStartedAt": "2021-07-11T21:33:10Z"
        }
        ],
        "reconciledAt": "2021-07-11T21:33:15Z",
        "operationState": {
        "operation": {
            "sync": {
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "prune": True,
            "syncOptions": [
                "Validate=false",
                "ApplyOutOfSyncOnly=true",
                "CreateNamespace=true"
            ]
            },
            "initiatedBy": {
            "automated": True
            },
            "retry": {
            "limit": 5
            }
        },
        "phase": "Succeeded",
        "message": "successfully synced (all tasks run)",
        "syncResult": {
            "resources": [
            {
                "group": "apps",
                "version": "v1",
                "kind": "Deployment",
                "namespace": "teste",
                "name": "nginx-ledivan-app",
                "status": "Synced",
                "message": "deployment.apps/nginx-ledivan-app configured",
                "hookPhase": "Running",
                "syncPhase": "Sync"
            }
            ],
            "revision": "cf19b85121a940a5ef7da2d3b31c165566d58e9c",
            "source": {
            "repoURL": "git@github.com:Marquesledivan/nginx_k8s.git",
            "path": "ledivan-app",
            "targetRevision": "HEAD",
            "helm": {
                "parameters": [
                {
                    "name": "image.tag",
                    "value": "1.20.0"
                }
                ]
            }
            }
        },
        "startedAt": "2021-07-11T21:33:10Z",
        "finishedAt": "2021-07-11T21:33:15Z"
        },
        "sourceType": "Helm",
        "summary": {
        "images": [
            "nginx:1.20.0"
        ]
        }
    }
    }
    payload = json.dumps(data)
    response = requests.put('https://127.0.0.1:8080/api/v1/applications/nginx', headers=headers, cookies=cookies, data=payload, verify=False)
    print(response.text)


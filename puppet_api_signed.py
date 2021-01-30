#!/usr/local/bin/python3

import requests
import pprint
import json
import sys
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

certs = "/etc/puppetlabs/puppet/ssl/certs/"
private_keys = "/etc/puppetlabs/puppet/ssl/private_keys/"
state = "requested"
db_hosts = []
unsigned = []
os = "ubuntu"

def puppet_db():
    try:
        db_hosts = []
        headers = {'Content-type': 'application/json'}
        r = requests.get("http://master.ledivan.com.br:8080/pdb/query/v4/nodes",headers=headers)
        for i in r.json():
            db_hosts.append(i["certname"])
        return db_hosts
    except json.decoder.JSONDecodeError as e:
        print(e)

def get_certificados(hosts):
    try:
        headers = {'Content-type': 'application/json'}
        r = requests.get(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_status/{hosts}' \
        ,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
        d = r.json()
        print(d["state"] + " "  + d["name"])
    except json.decoder.JSONDecodeError as e:
        print(e)

def certificados_status():
    unsigned = []
    try:
        headers = {'Content-type': 'application/json'}
        r = requests.get(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_statuses/any_key' \
        ,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
        for i in r.json():
            unsigned.append(i['name'])
    except json.decoder.JSONDecodeError as e:
        print(e)
    return unsigned

def get_unsigned():
    try:
        headers = {'Content-type': 'application/json'}
        r = requests.get(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_statuses/ignored?state={state}' \
        ,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
        for i in json.loads(r.text):
            if os in i["name"]:
                unsigned.append(i["name"])
    except json.decoder.JSONDecodeError as e:
        print(e)

def get_signed(hosts):
    try:
        headers = {'Content-type': 'application/json'}
        data = {"desired_state":"signed"}
        payload = json.dumps(data)
        r = requests.put(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_status/{hosts}' \
        ,data=payload,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
        print(r.text)
    except json.decoder.JSONDecodeError as e:
        print(e)

def revoked_certs(hosts):
    try:
        headers = {"Content-Type": "text/pson"}
        data = {"desired_state":"revoked"}
        payload = json.dumps(data)
        r = requests.put(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_status/{hosts}' \
        ,data=payload,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
        r = requests.delete(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_status/{hosts}' \
        ,data=payload,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
    except json.decoder.JSONDecodeError as e:
        print(e)

if __name__ == "__main__":
    arg = str(sys.argv[1])
    if arg == "delete":
        puppetdb = puppet_db()
        certificados = certificados_status()
        for nodes in certificados:
            if nodes not in puppetdb and nodes.startswith(os):
                print("revoked_certs", nodes)
                revoked_certs(nodes)
    elif arg == "get":
        print(certificados_status())
    elif arg == "sign":
        get_signed(sys.argv[2])

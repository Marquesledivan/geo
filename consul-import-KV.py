# -*- coding: utf-8 -*-

"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import os
import sys
import requests,json
from subprocess import check_output
import consul

APP_NAME=os.environ.get("APP_NAME").lower().replace("_","-")
keys_pairs_ti = os.environ.get("keys_pairs_ti")
keys_pairs_qa = os.environ.get("keys_pairs_qa")
keys_pairs_prod = os.environ.get("keys_pairs_prod")
CONSUL_TOKEN_PROD = os.environ.get("CONSUL_TOKEN_PROD")

def consul_input(*args):
    print('########## Autenticado no Consul de {0} ##########'.format(args[0]))
    client = consul.Consul(host=args[1], port=8500, token=args[2], scheme='http')
    keys_pairs = args[3]
    keys_pairs = keys_pairs.split(',|,')
    index = len(keys_pairs)
    if len(keys_pairs[index-1]) == 0:
        del keys_pairs[-1]
    slack_key = keys_pairs[0].split('/')
    slack("Backup do dados de ", slack_key[0], args[1], args[0] )
    for value in keys_pairs:
        if (keys_pairs.index(value) % 2) == 0:
            key = value
        else:
            client.kv.put(key, value.replace('\\"', '"'))
    slack("Update dos dados de ", slack_key[0], args[1], args[0])

def slack(*args):
    print('########## Enviando dados para Slack ##########')
    key = args[1]
    #json_key = check_output('consul kv export -http-addr={1}:8500 {0}/ | jq "."'.format(key[0],args[1]), shell=True).decode("utf-8")
    json_key = check_output('consul kv get -recurse -http-addr={1}:8500 {0}/'.format(key,args[2]), shell=True).decode("utf-8")
    url = 'slack'
    slack_header = "############### Consul KV Add/Update ###############"
    slack_body = "\n {0}{1}: \n {2} ".format(args[0], args[3], json_key )
    slack_footer = "\n##################################################"
    slack_text = "{0}{1}{2}".format(slack_header, slack_body, slack_footer)
    slack_data = {'text': slack_text, 'username': 'Tony', 'icon_emoji': ':tony_face','channel': APP_NAME}
    r = requests.post(url, data=json.dumps(slack_data))

if keys_pairs_ti is not None:
    consul_input("TI","url", None, str(keys_pairs_ti))
if keys_pairs_qa is not None:
    consul_input("QA", "url", None, str(keys_pairs_qa))
if keys_pairs_prod is not None:
    consul_input("PROD", "url", CONSUL_TOKEN_PROD, str(keys_pairs_prod))

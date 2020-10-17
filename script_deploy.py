#!/bin/python2.7
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br

"""
import requests
import json
import base64
import os
from os import system as sudo

TOKEN_CONSUL=os.environ.get("TOKEN_CONSUL")
CONSUL_HOST=os.environ.get("CONSUL_HOST")

headers = {'X-Consul-token': TOKEN_CONSUL}

class GET_URL:
    def __init__(self,path):
        self.url_consul = requests.get( CONSUL_HOST + path,headers=headers)
        self.consul = json.loads(self.url_consul.text)
        self.decode = base64.decodestring(str(self.consul[0]['Value']))
 
PATHRPASSWORD = GET_URL("/v1/kv/system/pathrpassword")
OHSOWNER = GET_URL("/v1/kv/system/owner")

def start_system():
   sudo('sed -i s/__endpoint_logstash__/{0}/ {1}'.format(GET_URL("/v1/kv/system/endpoint_logstash").decode,GET_URL("/v1/kv/system/rsyslog_path").decode))
   sudo('{0} start'.format(GET_URL("/v1/kv/system/ohs").decode))
   sudo('echo {0} > {1}'.format(GET_URL("/v1/kv/system/rpassword").decode,PATHRPASSWORD.decode))
   sudo('chmod 700 {0}'.format(PATHRPASSWORD.decode))
   sudo('chown -R {0}:{1} {2}'.format(OHSOWNER.decode,GET_URL("/v1/kv/system/oinstall").decode,PATHRPASSWORD.decode))
   sudo('su - {0} -c {1} &'.format(OHSOWNER.decode,GET_URL("/v1/kv/system/sync_system").decode))
   sudo('{0}'.format(GET_URL("/v1/kv/system/rsyslogd").decode))
   sudo('nginx -g "daemon off;"')

if __name__ == "__main__":
    start_system()

# -*- coding: utf-8 -*-
#!/usr/bin/python2.7
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import pymssql
import os
import httplib
import sys
import argparse
from enum import Enum
from subprocess import check_call, check_output, CalledProcessError

global jenkinscli
Script=os.environ.get("Script")
PWD_SUB=os.environ.get("PWD_SUB")
JENKINS_USER=os.environ.get('JENKINS_USER')
JENKINS_PASSWORD=os.environ.get('JENKINS_PASSWORD')
JENKINS_URL=os.environ.get('JENKINS_URL')
BUILD_URL=os.environ.get('BUILD_URL')
BUILD_DISPLAY_NAME=os.environ.get('BUILD_DISPLAY_NAME')
BUILD_ID=os.environ.get('BUILD_ID')

global statusbuilds
statusbuilds={}

class StatusBuild(Enum):
    SUCCESS=0
    UNSTABLE=1
    FAILURE=2
    NO_SUCH_JOB_NAME=3
    ABORTED=4
    JOB_PERMISSION_DENIED=6
    ERROR=7

def validate():
    if ("parity" or "money") and "where" in Script.lower():
        print ("Validação OK")
    else:
        raise Exception("\nErro de validação\n")
        sys.exit(1)

def altera_paridade():
    cnx = pymssql.connect(server='db_url',port=1433, user='user',password=PWD_SUB, database='Framework')
    cnx.autocommit(True)
    query = Script
    query_bkp = """select ConfigKey as ConfigKey,ConfigValue as ConfigValue from Config where ConfigKey like '%Livelo%' order by ConfigKey desc"""
    cursor = cnx.cursor()
    cursor.execute(query_bkp)
    res = cursor.fetchall()
    '''Exibir backup no log antes da execução do script'''
    print('Backup:  ')
    for i in range(len(res)):
        print(res[i])
    '''Execução do Script'''
    cursor.execute(query)

    try:
        cnx.commit()
        cnx.close()
    except Exception, e:
        print e
        pass

validate()
altera_paridade()

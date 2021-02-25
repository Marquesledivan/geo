#!/bin/python2.7
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br

"""

import os
import boto3
from time import sleep

access_key=os.environ.get("access_key")
secret_key=os.environ.get("secret_key")

REGIAO='sa-east-1'
boto3.setup_default_session(aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name=REGIAO)
region_list = ['sa-east-1']
for region in region_list:
    print('REGION:', region)
    ec2 = boto3.resource('ec2', region)
    for instance in ec2.instances.all():
        print('Instance:', instance)
        ec2tags = instance.tags
        TGS = []
        for t in ec2tags:
           if "aws:" in t["Key"]:
             rem = ec2tags.index(t)
           else:
                TGS.append(t)
        print('Tags:', TGS)
        for volume in instance.volumes.all():
            print('Volume:', volume)
            if volume.tags != TGS:
                print('\033[93m' + 'Tags don\'t match, updating')
                volume.create_tags(Tags=TGS)
            print('Tags:', volume.tags)
        print("Wait for 30 sec...")
        sleep(30)

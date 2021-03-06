#!/usr/local/bin/python3
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import boto3
import botocore
import pprint
client = boto3.client("ssm")

response = client.get_paginator('describe_parameters')
paginator = response.paginate().build_full_result()

lista = []
dirs = {'Key': "string", "Value": "string"}
for page in paginator['Parameters']:
    response = client.get_parameter(Name=page['Name'])
    value = response['Parameter']['Value']
    lista.append(page['Name'])

def set_tags():
    string = "string"
    TGS = {}
    for i in lista:
        tags = client.list_tags_for_resource(
            ResourceType='Parameter',
            ResourceId=i
        )
        try:
            for r in tags['TagList']:
                if "string" in r["Key"]:
                    TGS.update({'Key': "string", "Value": r["Value"]})
                    break
                else:
                    TGS.update(dirs)
                    break
            if TGS not in tags['TagList']:
                print(i)
                client.add_tags_to_resource(ResourceType='Parameter',ResourceId=i,Tags=[TGS])
        except botocore.exceptions.ParamValidationError:
            print(i)
            client.add_tags_to_resource(ResourceType='Parameter',ResourceId=i,Tags=[dirs])

set_tags()

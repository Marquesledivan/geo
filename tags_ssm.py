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

def get_tags(name):
    string = "string"
    tags = client.list_tags_for_resource(
        ResourceType='Parameter',
        ResourceId=name
    )
    for r in tags['TagList']:
        if "string" in r["Key"]:
            tag = {'Key': string, "Value": r["Value"]}
            return tag
    return dirs

def set_tags(tgs,name):
    tags = client.list_tags_for_resource(
        ResourceType='Parameter',
        ResourceId=name
    )
    try:
        if tgs not in tags['TagList']:
            print(name,tgs)
            client.add_tags_to_resource(ResourceType='Parameter',ResourceId=name,Tags=[tgs])
    except botocore.exceptions.ParamValidationError:
        print(name,tgs)
        client.add_tags_to_resource(ResourceType='Parameter',ResourceId=name,Tags=[tgs])

for parameter in lista:
    set_tags(get_tags(parameter),parameter)

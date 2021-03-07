#!/usr/local/bin/python3
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import boto3
import botocore
import pprint
REGION = ['us-east-1',"us-east-1"]


lista = []
tgs_name = {'Key': "string", "Value": "string"}

def region_get(regions):
    client = boto3.client("ssm",region_name=regions)
    response = client.get_paginator('describe_parameters')
    paginator = response.paginate().build_full_result()

    for page in paginator['Parameters']:
        response = client.get_parameter(Name=page['Name'])
        value = response['Parameter']['Value']
        lista.append(page['Name'])

def get_tags(name,regions):
    string = "string"
    client = boto3.client("ssm",region_name=regions)
    tags = client.list_tags_for_resource(
        ResourceType='Parameter',
        ResourceId=name
    )
    for r in tags['TagList']:
        if "string" in r["Key"]:
            tag = {'Key': string, "Value": r["Value"]}
            return tag
    return tgs_name

def set_tags(tgs,name,regions):
    client = boto3.client("ssm",region_name=regions)
    tags = client.list_tags_for_resource(
        ResourceType='Parameter',
        ResourceId=name
    )
    try:
        if tgs not in tags['TagList']:
            client.add_tags_to_resource(ResourceType='Parameter',ResourceId=name,Tags=[tgs])
            print(name,tgs)
    except botocore.exceptions.ParamValidationError:
        client.add_tags_to_resource(ResourceType='Parameter',ResourceId=name,Tags=[tgs])
        print(name,tgs)

for reg in REGION:
    region_get(reg)
    for parameter in lista:
        set_tags(get_tags(parameter,reg),parameter,reg)

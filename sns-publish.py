import json
import boto3

message = { "Key": "Ledivan", "Value": "Bernardo" }
client = boto3.client('sns')

response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:434842609133:ledivan_teste',
    Message=json.dumps(message),
    Subject='teste',
)


if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
     print('Sucesso!!!')
 

## aws sns publish --topic-arn "arn:aws:sns:us-east-1:434842609133:ledivan_teste" --message '{ "Key": "BOB", "Value": "BOB" }'
##############################################################################################################################

#!/usr/local/bin/python3
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import boto3
import botocore
import pprint
import json
ec2 = boto3.client('ec2')
regions = ec2.describe_regions()

def parameter_by_region(client):
    lista = []
    response = client.get_paginator('describe_parameters')
    paginator = response.paginate().build_full_result()
    for page in paginator['Parameters']:
        response = client.get_parameter(Name=page['Name'])
        value = response['Parameter']['Value']
        lista.append(page['Name'])
    return lista

def get_tags(name,client):
    string = "string"
    tags = client.list_tags_for_resource(
        ResourceType='Parameter',
        ResourceId=name
    )
    for r in tags['TagList']:
        if len(tags['TagList']) > 0 and "string" in r["Key"]:
            return True
    return False


def set_tags(get_tags,name,client,tgs_name):
    tags = client.list_tags_for_resource(
        ResourceType='Parameter',
        ResourceId=name
    )
    if not get_tags:
        print(f"Building {name} tags............")
        client.add_tags_to_resource(ResourceType='Parameter',ResourceId=name,Tags=[tgs_name])

def lambda_handler(event, context):
    message = json.loads(event["Records"][0]['Sns']["Message"])
    tgs_name = {'Key': message["Key"], "Value": message["Value"]}
    for region in regions['Regions']:
        if region["RegionName"] in "us-east-1":
            print("Region: " + str(region['RegionName']))
            client = boto3.client("ssm",region_name=region['RegionName'])
            for parameter_name in parameter_by_region(client):
                tags_owner = get_tags(parameter_name,client)
                set_tags(tags_owner,parameter_name,client,tgs_name)

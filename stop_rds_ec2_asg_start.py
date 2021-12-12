#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import boto3 as session
import json
import os
import traceback 

STATE_NAME = os.getenv("STATE_NAME")
TAGS_KEY = os.getenv("TAGS_KEY")
TAGS_VALUE = os.getenv("TAGS_VALUE")

def parameters_store(method, *argv):
    client = session.client('ssm')
    if method == "put":
        client.put_parameter(Name=STATE_NAME,Description='ASG status before stop',Value=json.dumps(argv[0]),Type='String',Overwrite=True,)
    if method == "get":
        return(client.get_parameter(Name=STATE_NAME))


def updaterds(action):
    client = session.client('rds')
    response = client.get_paginator('describe_db_instances')
    paginator = response.paginate().build_full_result()
    for dbinstances in paginator["DBInstances"]:
        for tags in dbinstances["TagList"]:
            if tags["Key"] == TAGS_KEY and tags["Value"] == TAGS_VALUE:
                if action == "start" and dbinstances["DBInstanceStatus"] == "stopped":
                    print("updated instance start:", dbinstances["DBInstanceIdentifier"])  
                    client.start_db_instance(DBInstanceIdentifier=dbinstances["DBInstanceIdentifier"])
                if action == "stop" and dbinstances["DBInstanceStatus"] == "available":    
                    print("updated instance stop:", dbinstances["DBInstanceIdentifier"])  
                    client.stop_db_instance(DBInstanceIdentifier=dbinstances["DBInstanceIdentifier"])

def updateec2(action):
    client = session.client('ec2')
    instanceIds = []
    if action == "stop":
        state = "running"
    if action  == "start":
        state = "stopped"
    else:
        print('Invalid option please validate EC2 state')

    response = client.get_paginator('describe_instances')
    paginator = response.paginate().build_full_result()
    for reservation in paginator['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == state and not instance['Tags'] is None:
                for tag in instance['Tags']:
                    try:
                        if tag['Key'] == TAGS_KEY and tag['Value'] == TAGS_VALUE not in "aws:autoscaling:groupName":
                            instanceIds.append(instance['InstanceId'])
                    except:
                        print("Not expected error: ", traceback.print_exc())                        
        if len(instanceIds) > 0 and action == "start": 
            print("Starting instances: " + str(instanceIds))
            client.start_instances(InstanceIds=instanceIds)     
        if len(instanceIds) > 0 and action == "stop": 
            print("Stopping instances: " + str(instanceIds))
            client.stop_instances(InstanceIds=instanceIds)

def asg_update(action):
    list_asg = []
    client = session.client('autoscaling')
    response = client.get_paginator('describe_auto_scaling_groups')
    paginator = response.paginate().build_full_result()
    for asg in paginator["AutoScalingGroups"]:
        if not asg["Tags"] is None:
            for tags in asg["Tags"]:
                if tags["Key"] == TAGS_KEY and tags['Value'] == TAGS_VALUE and action == "stop" and asg["MaxSize"] > 0:
                    list_asg.append({"name" : asg["AutoScalingGroupName"], "min" : asg["MinSize"], "max" : asg["MaxSize"], "des" : asg["DesiredCapacity"]})
                    parameters_store("put",list_asg)
    if len(list_asg) > 0 and action == "stop" and asg["MaxSize"] > 0:
        for asg_list in list_asg:
            print("Resetting the asg",asg_list["name"])
            client.update_auto_scaling_group(AutoScalingGroupName=asg_list["name"],MinSize=0,MaxSize=0,DesiredCapacity=0)
    if len(list_asg) == 0 and action == "start" and asg["MaxSize"] == 0:
        getparameter = json.loads(parameters_store("get")["Parameter"]["Value"])
        for asg_list in getparameter:
            print("Going up asg",asg_list["name"])
            client.update_auto_scaling_group(AutoScalingGroupName=asg_list["name"],MinSize=asg_list["min"],MaxSize=asg_list["max"],DesiredCapacity=asg_list["des"])


def lambda_handler(event, context):
    if len(event["action"]) > 0:
        print("Starting process: ")
        asg_update(event["action"])
        updaterds(event["action"])
        updateec2(event["action"])

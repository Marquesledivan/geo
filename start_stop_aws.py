#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import boto3
import pprint
import json
import sys, traceback

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()

instanceIds = []

def get_instances():
  for r in response["Reservations"]:
        for i in r["Instances"]:
          for tag in i["Tags"]:
                if tag["Key"] == 'Name':
                  t = i["InstanceType"]
                  v  = tag['Value']
                  s = i["State"]["Name"]
                  print (f'InstanceType: {t} name: {v}  state: {s} ')

def get_start():
    for reservation in response['Reservations']:
          for response in reservation['Instances']:
                      for state in response["State"]["Name"]:
                            try:
                              if response['State']['Name'] == "stopped":
                                    instanceIds.append(response['InstanceId'])
                            except:
                                  print ("Not expected error: ", traceback.print_exc())
          if len(instanceIds) > 0:
              print ("Starting instances: " + str(instanceIds))
              ec2client.stop_instances(InstanceIds=instanceIds)

def get_stop():
    for reservation in response['Reservations']:
          for response in reservation['Instances']:
                      for state in response["State"]["Name"]:
                            try:
                              if response['State']['Name'] == "running":
                                    instanceIds.append(response['InstanceId'])
                            except:
                                  print ("Not expected error: ", traceback.print_exc())
          if len(instanceIds) > 0:
              print ("Stopping instances: " + str(instanceIds))
              ec2client.stop_instances(InstanceIds=instanceIds)
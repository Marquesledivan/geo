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
import argparse

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()

instanceIds = []

parser = argparse.ArgumentParser()
parser.add_argument('--type', help='Check the get, start or stop parameters')
args = parser.parse_args()

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
    response = ec2client.describe_instances()
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
              ec2client.start_instances(InstanceIds=instanceIds)

def get_stop():
    response = ec2client.describe_instances()
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

if __name__ == "__main__":
    print('Starting instances... ')
    if args.type == "get":
          get_instances()
    elif args.type == "start":
          get_start()
    elif args.type ==  "stop":
          get_stop()
    else:
      print("Please check the parameters --type: get, start or stop")

#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import requests
import base64
import json
import os
import boto3
import shutil 
from datetime import datetime, timedelta

user = ""
encoded  = str(base64.urlsafe_b64encode(user.encode("utf-8")),"utf-8")
headers = {'authorization': f'Basic {encoded}' }
url = ""
dir_name = "dir_apis" 
bucket_name = "" 
s3_client = boto3.client('s3')
now = datetime.now()
dt_string = now.strftime("%m-%d-%y_%H-%M-%S")
apis = "apis-"+dt_string

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

def main():
    ids = []
    response = requests.get(f'{url}/management/organizations/DEFAULT/environments/DEFAULT/apis', headers=headers)
    for id in json.loads(response.text):
        ids.append(id['id'])

    for api in ids:
        response = requests.get(f'{url}/management/organizations/DEFAULT/environments/DEFAULT/apis/' + api +'/export', headers=headers)
        payload = json.dumps(response.json())
        api_name = response.json()["name"]
        print(api_name)
        with open(dir_name + "/" + api_name + ".json", "w") as file:
            file.write(payload)
            file.close()
    
    # Zip archive
    shutil.make_archive(apis, 'zip', './', dir_name)
    _bucket("apis", apis + ".zip")

def _bucket(s3_folder,local_file_path):
  s3 = boto3.resource('s3')
  if s3.Bucket(bucket_name) not in s3.buckets.all():
     s3_client.create_bucket(Bucket=bucket_name)
  s3_path = os.path.join(s3_folder, os.path.basename(local_file_path))
  s3.meta.client.upload_file(local_file_path, bucket_name, s3_path)
  response = s3_client.list_objects(Bucket=bucket_name)
  for content in response["Contents"]:
      lastmodified = (content["LastModified"]).replace(tzinfo = None)
      date_limit = datetime.now() - timedelta(int("0"))
      if lastmodified <= date_limit:
          s3_client.delete_objects(Bucket=bucket_name,Delete={'Objects': [{'Key': content["Key"]}]})
  if os.path.exists(apis+ ".zip"):
      os.remove(apis + ".zip")
  if os.path.exists(dir_name):
      shutil.rmtree(dir_name)

if __name__ == "__main__":
    main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan@cvc.com.br

"""

import boto3

session = boto3.Session(profile_name='ti-sa')
client = session.client('ecr')

def Untagged():
  response = client.get_paginator('describe_repositories')
  describe = response.paginate().build_full_result()
  try:
    for i in describe['repositories']:
      print("repository:", i['repositoryUri'].split("/")[1])
      response = client.list_images(registryId=i['registryId'],repositoryName=i['repositoryName'],filter={'tagStatus': 'UNTAGGED'})
      for imageDigest in response["imageIds"]:
        print("imageDigest", imageDigest['imageDigest'])
        print("Delete images Untagged from ECR",imageDigest['imageDigest'])
        client.batch_delete_image(registryId=i['registryId'],repositoryName=i['repositoryName'],imageIds=[{'imageDigest':imageDigest['imageDigest']},])
  except Exception as a:
    print("Erro {0}".format(a))

if __name__ == "__main__":
  Untagged()

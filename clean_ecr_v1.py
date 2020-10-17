#!/bin/python2.7
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import subprocess

result = subprocess.check_output("""aws ecr describe-repositories --query 'repositories[*].repositoryName' --profile desenvolvimento | jq .[] | sed 's|"||g'""", shell=True)

def ecr():
     for repo in result.splitlines():         
         TAGS=subprocess.check_output("""aws ecr list-images --region sa-east-1 --repository-name """ + repo + """ --filter tagStatus=UNTAGGED --query 'imageIds[].imageDigest' --profile desenvolvimento | jq .[] | sed 's|"||g'""",shell=True)
         for tag in TAGS.splitlines():
             print("Deleting image:" + tag)
             subprocess.call("aws ecr batch-delete-image --region sa-east-1 --repository-name " + repo + " --image-ids imageDigest="+tag+" --profile desenvolvimento",shell=True)
        
if __name__ == "__main__":
     ecr()

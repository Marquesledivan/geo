#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
from flask import Flask, request, jsonify
from flask_api import FlaskAPI, status, exceptions
import boto3
import json
import pprint
import botocore

client = boto3.client('ec2')
reponse = client.describe_instances()

app = Flask(__name__)

lista = []
@app.route('/', methods=['GET'])
def get_nome():
    lista.clear()
    if request.method == 'GET':
        for i in reponse["Reservations"]:
            for instace in i["Instances"]:
                ids = instace["InstanceId"] + ', ' + instace["State"]["Name"]
                lista.append(ids)
        return jsonify(lista)

stopped = "stopped"
@app.route("/stopped", methods=['POST'])
def stop():
    if request.method == 'POST':
        if request.is_json:
            content = request.get_json()
            instancia = content["InstanceIds"]["id"]
            try:
                for i in instancia:
                    state = client.describe_instances(InstanceIds=[i])
                    if state["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        if content['InstanceIds']['state'] == stopped:
                            try:
                                if len(instancia) > 0:
                                    for i in instancia:
                                        client.stop_instances(InstanceIds=[i],DryRun=False)
                            except ClientError as e:
                                if 'DryRunOperation' not in str(e):
                                    raise
                            finally:
                                return jsonify(stopped,instancia), status.HTTP_201_CREATED
            except botocore.exceptions.ClientError as e:
                return "HTTP_404_NOT_FOUND", status.HTTP_404_NOT_FOUND

if __name__ == '__main__':
    app.run(debug=True)

#### curl --location --request POST 'http://127.0.0.1:5000/stopped' --header 'Content-Type: application/json' --data-raw '{ "InstanceIds": { "state": "stopped", "id": ["i-00000000","i-111111111"] }}'

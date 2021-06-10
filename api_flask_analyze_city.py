#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import csv
import requests
import os
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
import urllib.request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

url_ibge = r"http://blog.mds.gov.br/redesuas/wp-content/uploads/2018/06/Lista_Munic%C3%ADpios_com_IBGE_Brasil_Versao_CSV.csv"

def states(sigla):
      response = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
      for siglas in response.json():
            if sigla in siglas["sigla"]:
                  return siglas["nome"]
def get(sigla):
      lista = ""
      with urllib.request.urlopen(url_ibge) as entrada:
        print("Downloading data for analysis")
        dados = entrada.read().decode('latin-1')
        for cidade in csv.reader(dados.splitlines(True)):
              si = f'{cidade[0]}'
              ci_sigla = si.split(";")
              if sigla.upper() in  ci_sigla:
                    lista += ('\n'+ci_sigla[0][2:])
        return lista

def send_email(sigla_city):
      sigla = states(sigla_city.upper())
      body = str(get(sigla_city.upper()))
      html = f"""
            <html>
            <body>
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b3/Rua_do_Conjunto_Arquitet%C3%B4nico_da_Cidade_de_Goi%C3%A1s%2C_Goi%C3%A1s%2C_Brasil.jpg" width="522" height="346">
            </body>
            </html>
            <html> <body> <p>Hi,<br>Check out the new post on the api city blog:</p> <p><a href="https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla_city.upper()}">Test API: Cloud-based or City API!!</a></p> <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p> </body> </html> <pre>
            <p style="font-size:30px">"""+sigla +"""</p>
            """+ body +"""
      """
      gmail_user = ''
      gmail_password = ''
      to = ''
      message = MIMEMultipart("alternative")
      message["Subject"] = f'State {sigla}'
      message["From"] = gmail_user
      message["To"] = to

      sent_from = gmail_user
      try:
            message.attach(MIMEText(html, "html"))
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to,message.as_string())
            server.close()
            return "Email sent!"
      except:
            return "Failed to send email"
@app.route('/state', methods=['POST'])
def state_city():
      try:
            content = request.get_json()
            return send_email(content["state"])
      except:
            return 'Call Failed'

if __name__ == '__main__':
    app.run(debug=True)

## call api

import requests
import json
url = "http://127.0.0.1:5000/state"

dados={ "state": "go" }
payload = json.dumps(dados)
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import csv
import requests
from urllib import request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import sys

city =  sys.argv[1]

url_ibge = r"http://blog.mds.gov.br/redesuas/wp-content/uploads/2018/06/Lista_Munic%C3%ADpios_com_IBGE_Brasil_Versao_CSV.csv"
html = f"""
<html>
<body>
<img src="https://upload.wikimedia.org/wikipedia/commons/b/b3/Rua_do_Conjunto_Arquitet%C3%B4nico_da_Cidade_de_Goi%C3%A1s%2C_Goi%C3%A1s%2C_Brasil.jpg" width="522" height="346">
</body>
</html>
<html> <body> <p>Hi,<br>Check out the new post on the api city blog:</p> <p><a href="https://servicodados.ibge.gov.br/api/v1/localidades/estados/{city.upper()}">Test API: Cloud-based or City API!!</a></p> <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p> </body> </html> <pre>
"""

def states(sigla):
      response = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
      for siglas in response.json():
            if sigla in siglas["sigla"]:
                  return siglas["nome"]
def get(url):
      count = 0
      list_cidades = []
      sigla_city = states(city.upper())
      if os.path.exists("demofile.txt"):
            os.remove("demofile.txt")
      f = open("demofile.txt", "a")
      f.write(html)
      f.write("""<p style="font-size:30px">"""+sigla_city +"""</p>""")
      with request.urlopen(url) as entrada:
        print("Downloading data for analysis")
        dados = entrada.read().decode('latin-1')
        for cidade in csv.reader(dados.splitlines(True)):
              sigla = f'{cidade[0]}'
              ci_sigla = sigla.split(";")
              if city.upper() in  ci_sigla:
                    f = open("demofile.txt", "a")
                    f.write('\n'+ci_sigla[0][2:])
                    f.close()

def send_email(url):
      gmail_user = ''
      gmail_password = ''
      to = ''
      message = MIMEMultipart("alternative")
      sigla_city = states(city.upper())
      message["Subject"] = f'State {sigla_city}'
      message["From"] = gmail_user
      message["To"] = to

      body = str(get(url))
      with open("demofile.txt", "r") as read:
            bodys = read.read()
      sent_from = gmail_user
      try:
            message.attach(MIMEText(bodys, "html"))
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to,message.as_string())
            server.close()

            print("Email sent!")
      except:
            print("Failed to send email")

if __name__ == "__main__":
      send_email(url_ibge)

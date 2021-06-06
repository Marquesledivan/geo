#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import csv
from urllib import request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

url_ibge = r"http://blog.mds.gov.br/redesuas/wp-content/uploads/2018/06/Lista_Munic%C3%ADpios_com_IBGE_Brasil_Versao_CSV.csv"
html_ = """
<html>
<body>
<img src="https://upload.wikimedia.org/wikipedia/commons/b/b3/Rua_do_Conjunto_Arquitet%C3%B4nico_da_Cidade_de_Goi%C3%A1s%2C_Goi%C3%A1s%2C_Brasil.jpg" width="522" height="346">
</body>
</html>
<html> <body> <p>Hi,<br> Check out the new post on the Mailtrap blog:</p> <p><a href="https://blog.mailtrap.io/2018/09/27/cloud-or-local-smtp-server">SMTP Server for Testing: Cloud-based or Local?</a></p> <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p> </body> </html> <pre>
"""

def get(url):
      count = 0
      list_cidades = []
      if os.path.exists("demofile.txt"):
            os.remove("demofile.txt")
      f = open("demofile.txt", "a")
      f.write(html_)
      f.write("""<p style="font-size:30px">Goiás</p>""")
      with request.urlopen(url) as entrada:
        print("Downloading data for analysis")
        dados = entrada.read().decode('latin-1')
        for cidade in csv.reader(dados.splitlines(True)):
              sigla = f'{cidade[0]}'
              ci_sigla = sigla.split(";")
              if "GO" in  ci_sigla:
                    f = open("demofile.txt", "a")
                    f.write('\n'+ci_sigla[0][2:])
                    f.close()
                    list_cidades.append(ci_sigla[0][2:])
      return list_cidades

def send_email(url):
      gmail_user = ''
      gmail_password = ''
      to = ''
      message = MIMEMultipart("alternative")
      message["Subject"] = "State Goiás"
      message["From"] = gmail_user
      message["To"] = to

      body = str(get(url))
      with open("demofile.txt", "r") as read:
            bodys = read.read()
      sent_from = gmail_user
      with open('download.jpeg', 'rb') as img:
            image = MIMEImage(img.read())
      image.add_header('Content-ID', '<myimage>')
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
      print("Starting analysis")
      send_email(url_ibge)

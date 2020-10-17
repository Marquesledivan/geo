# -*- coding: utf-8 -*-
#!/usr/bin/python2.7

import pymssql
import os

Amadeus=os.environ.get("AM")
LA=os.environ.get("LA")
FRT=os.environ.get("FRT")
AmericanAirlines=os.environ.get("FL")
Gol=os.environ.get("G3")
Sabre=os.environ.get("SB")
Avianca=os.environ.get("AV")
Azul=os.environ.get("AD")
Passaredo=os.environ.get("2Z")

strCias=''
if Amadeus.upper() == 'TRUE':
   strCias += 'AM,'
if LA.upper() == 'TRUE':
   strCias += 'LA,'
if FRT.upper() == 'TRUE':
   strCias += 'FRT,'
if AmericanAirlines.upper() == 'TRUE':
   strCias += 'FL,'
if Gol.upper() == 'TRUE':
   strCias += 'G3,'
if Sabre.upper() == 'TRUE':
   strCias += 'SB,'
if Avianca.upper() == 'TRUE':
   strCias += 'AV,'
if Azul.upper() == 'TRUE':
   strCias += 'AD,'
if Passaredo.upper() == 'TRUE':
   strCias += '2Z,'
###Retirar a vírgula do final 
strCias = strCias[0:len(strCias)-1]

db = pymssql.connect(server='url_db',port=1433, user='user',password='passwd', database='Framework')
db.autocommit(True)
cur = db.cursor()

comando = "select ConfigValue from Config where ConfigKey ='ledivan'"
cur.execute(comando)
res = cur.fetchall()
print('Segue backup da chave:')
for i in range(len(res)):
    print(res[i])

comando1 = "update Config set ConfigValue = '" + strCias + "' where ConfigKey = 'ledivan'" 
print(comando1)
cur.execute(comando1)


print('CIAS presentes na chave:' + strCias)
db.close()

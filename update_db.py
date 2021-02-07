#!/usr/bin/python3.6
# coding: utf-8
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import pymssql
import os

Notify=os.environ.get("Notify")
AmericanAirlines=os.environ.get("AmericanAirlines")
Package=os.environ.get("Package")
Hotel=os.environ.get("Hotel")
Passaredo=os.environ.get("Passaredo")
Gol=os.environ.get("Gol")
Sabre=os.environ.get("Sabre")
Avianca=os.environ.get("Avianca")
Azul=os.environ.get("Azul")
RexturAdvance=os.environ.get("RexturAdvance")
Latam=os.environ.get("Latam")
instancias=os.environ.get("instancias")

strCias=''
if AmericanAirlines.upper() == 'TRUE':
   strCias += 'AmericanAirlines,'
if Notify.upper() == 'TRUE':
   strCias += 'Tam,Notify_CION,Notify_GOL,Notify_FLX,Notify_AZUL,Notify_AVI,Notify_SAB,MAP,'
if Package.upper() == 'TRUE':
   strCias += 'Package,'
if Hotel.upper() == 'TRUE':
   strCias += 'Hotel,'
if Passaredo.upper() == 'TRUE':
   strCias += 'Passaredo,'
if Gol.upper() == 'TRUE':
   strCias += 'Gol,'
if Sabre.upper() == 'TRUE':
   strCias += 'Sabre,'
if Avianca.upper() == 'TRUE':
   strCias += 'Avianca,'
if Azul.upper() == 'TRUE':
   strCias += 'Azul,'
if RexturAdvance.upper() == 'TRUE':
   strCias += 'RexturAdvance,'
if Latam.upper() == 'TRUE':
   strCias += 'Latam,'
###Retirar a vírgula do final
strCias = strCias[0:len(strCias)-1]

db = pymssql.connect(server=instancias,port=1433, user='',password='', database='Framework')
db.autocommit(True)
cur = db.cursor()

comando = "select ConfigKey,ConfigValue from Config where ConfigKey in ('NotAirTask','NoAirHotelTask')"
cur.execute(comando)
res = cur.fetchall()
print('Segue backup da chave:')
for i in range(len(res)):
    print(res[i])

comando1 = "update Config set ConfigValue = '" + strCias + "' where ConfigKey = 'NotAirTask'" 
print(comando1)
cur.execute(comando1)
comando2 = "update Config set ConfigValue = '" + strCias + "' where ConfigKey = 'NoAirHotelTask'"
print(comando2)
cur.execute(comando2)

print('CIAS presentes na chave:' + strCias)
db.close() 

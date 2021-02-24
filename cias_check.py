#!/usr/local/bin/python2.7
# coding: utf-8
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import cx_Oracle
from lxml import etree
from io import StringIO
import datetime, time,argparse
import requests
requests.packages.urllib3.disable_warnings()

start = time.time()

now = datetime.datetime.today()
oneweek = now + datetime.timedelta(days=14)
twoweeks = now + datetime.timedelta(days=21)

username = ''
password = ''
address  = ''
database = ''

db = cx_Oracle.connect('''{0}/{1}@{2}/{3}'''.format(username,password,address,database))
sql = " "
cur = db.cursor()
cur.execute(sql)
res = cur.fetchall()
for i in res:
	login = i[1]
	senha = i[2]

parser = argparse.ArgumentParser()
parser.add_argument('--tipo', help='Nacional ou Interfacional')
args = parser.parse_args()

url = " "

headers = {'Content-Type': 'text/xml;charset=UTF-8', 'SOAPAction': ''}
header_voo = {'Content-Type': 'text/xml;charset=UTF-8', 'SOAPAction': ''}

login = '''

'''.format(login,senha)

response = requests.post(url, data=login, headers=headers).content
tree = etree.XML(response)
result = (etree.tostring(tree, pretty_print=True))
SecurityToken = tree.xpath("//*[local-name() = 'SecurityToken']")[0].text
SessionID = tree.xpath("//*[local-name() = 'SessionId']")[0].text

nacional = '''

'''.format(SessionID,SecurityToken,oneweek.strftime('%d%m%y'),twoweeks.strftime('%d%m%y'))

internacional = '''

'''.format(SessionID,SecurityToken,oneweek.strftime('%d%m%y'),twoweeks.strftime('%d%m%y'))

if args.tipo == 'Nacional':
   response_voo = requests.post(url, data=nacional, headers=header_voo).content
   tree_voo = etree.XML(response_voo)
   result_voo = (etree.tostring(tree_voo, pretty_print=True))
   try:
      assert ('detalhesDeReferencia' in result_voo)
      end = time.time()
      print int(end - start)
   except Exception, error:
      print 'Erro'
else:
   response_voo = requests.post(url, data=internacional, headers=header_voo).content
   tree_voo = etree.XML(response_voo)
   result_voo = (etree.tostring(tree_voo, pretty_print=True))
   try:
      assert ('detalhesDeReferencia' in result_voo)
      end = time.time()
      print int(end - start)
   except Exception, error:
      print 'Erro'

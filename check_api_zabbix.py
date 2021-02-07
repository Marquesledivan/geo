#!/usr/bin/python3.6
# coding: utf-8
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
import requests
import datetime
import time
import argparse
from ZabbixSender import ZabbixSender, ZabbixPacket

server = ZabbixSender(' ', 10051)
packet = ZabbixPacket()

start = time.time()
now = datetime.datetime.today()
date_start = now + datetime.timedelta(days=35)
date_end = now + datetime.timedelta(days=45)

parser = argparse.ArgumentParser()
parser.add_argument('--tipo', help='Nacional ou Interfacional')
args = parser.parse_args()

url = " "

nacional = '''{{
 "Adults": "1",
 "Children": "0",
 "Infants": "0",
 "DirectFlight": "true",
 "ResultsQuantity": "50",
 "CityPairs": [
   {{
     "DepartureDate": {{
       "Day": "{0}",
       "Month": "{1}",
       "Year": "{2}"
     }},
     "DestinationIata": "SAO",
     "OriginIata": "SSA"
   }},
   {{
     "DepartureDate": {{
       "Day": "{3}",
       "Month": "{4}",
       "Year": "{5}"
     }},
     "DestinationIata": "SSA",
     "OriginIata": "SAO"
   }}
 ]
}}'''.format(date_start.strftime('%d'),date_start.strftime('%m'), date_start.strftime('%Y'), date_end.strftime('%d'), date_end.strftime('%m'), date_end.strftime('%Y'))

internacional = '''{{
 "Adults": "1",
 "Children": "0",
 "Infants": "0",
 "DirectFlight": "true",
 "ResultsQuantity": "50",
 "CityPairs": [
   {{
     "DepartureDate": {{
       "Day": "{0}",
       "Month": "{1}",
       "Year": "{2}"
     }},
     "DestinationIata": "SAO",
     "OriginIata": "MIA"
   }},
   {{
     "DepartureDate": {{
       "Day": "{3}",
       "Month": "{4}",
       "Year": "{5}"
     }},
     "DestinationIata": "MIA",
     "OriginIata": "SAO"
   }}
 ]
}}'''.format(date_start.strftime('%d'), date_start.strftime('%m'), date_start.strftime('%Y'), date_end.strftime('%d'), date_end.strftime('%m'), date_end.strftime('%Y'))

headers = {
    'Content-Type': "application/json",
    'x-api-key': " ",
    'cache-control': "no-cache"
    }

if args.tipo == 'Nacional':
   response_voo = requests.request("POST", url, data=nacional, headers=headers)
   result_voo = result = response_voo.text
   try:
      assert ('operatingAirlineCode' in result_voo)
      end = time.time()
      result_time = int(end - start)
      packet.add('NEGOCIOS','check_afiliados_nac', result_time)
   except Exception as error:
      packet.add('NEGOCIOS','check_afiliados_nac', 'Erro')
elif args.tipo == "Interfacional":
   response_voo = requests.request("POST", url, data=internacional, headers=headers)
   result_voo = result = response_voo.text
   try:
      assert ('operatingAirlineCode' in result_voo)
      end = time.time()
      result_time = int(end - start)
      packet.add('NEGOCIOS ','check_afiliados_int', result_time)
   except Exception as error:
      packet.add('NEGOCIOS','check_afiliados_int', 'Erro')

server.send(packet)

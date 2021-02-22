#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
from os import system as sudo
from datetime import date
import shutil
import os
today = date.today()

openssl = """[ca]
  default_ca     = CA_default            # The default ca section

[CA_default]
  database       = ./index.txt           # index file.
  new_certs_dir  = ./newcerts            # new certs dir

  certificate    = ./ca/ca_crt.pem
  serial         = ./serial
  default_md     = sha1                  # md to use
  policy         = CA_policy             # default policy
  email_in_dn    = no                    # Don't add the email
  name_opt       = ca_default            # SubjectName display option
  cert_opt       = ca_default            # Certificate display option
  x509_extensions = CA_extensions

[CA_policy]
  countryName            = optional
  stateOrProvinceName    = optional
  organizationName       = optional
  organizationalUnitName = optional
  commonName             = supplied
  emailAddress           = optional

[CA_extensions]
  nsComment            = "Puppet Cert: manual."
  basicConstraints     = CA:TRUE
  subjectKeyIdentifier = hash
  keyUsage             = keyCertSign, cRLSign
"""

def renew_ca_puppet():
    path = "/etc/puppetlabs/puppet/ssl"
    date = today.strftime("%d-%m-%Y")
    days = "3650"
    if not os.path.exists(f'{path}-bkp-{date}'):
        shutil.copytree(f'{path}',f'{path}-bkp-{date}')
    with open(f"{path}/openssl.cnf", "w") as f:
      f.write(openssl)
      f.close()
    with open(f"{path}/index.txt", 'a') as f:
      f.close()
    if not os.path.exists(f'{path}/newcerts'):
          os.makedirs(f'{path}/newcerts')
    with open(f'{path}/serial', "a") as f:
      f.write("00")
      f.close()
    sudo("""
    cd """+path+""" && \
    openssl x509 -x509toreq -in certs/ca.pem -signkey ca/ca_key.pem -out certreq.csr && \
    openssl ca -in certreq.csr -keyfile ca/ca_key.pem -days """+ days +""" -out newcert.pem -config ./openssl.cnf &&\
    cp -r """+path+"""/ca/ca_crt.pem{,.bak} && \
    cp newcert.pem ca/ca_crt.pem && \
    rm """+path+"""/certs/ca.pem && \
    rm -rfv certreq.csr index.txt* newcert* serial.old && \
    puppet agent -t
    """)

if __name__ == "__main__":
    renew_ca_puppet()

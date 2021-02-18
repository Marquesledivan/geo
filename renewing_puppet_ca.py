#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version 1.0 Author: Ledivan B. Marques
            Email:	ledivan_bernardo@yahoo.com.br
"""
from os import system as sudo
from datetime import date
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
    date = today.strftime("%m-%d-%Y")
    sudo(f'cp -r /etc/puppetlabs/puppet/ssl /etc/puppetlabs/puppet/ssl-bkp-{date}')
    with open("/etc/puppetlabs/puppet/ssl/openssl.cnf", "w") as f:
        f.write(openssl)
        f.close()
    sudo("""
    cd /etc/puppetlabs/puppet/ssl && \
    mkdir -p newcerts && touch index.txt && echo 00 > serial && \
    openssl x509 -x509toreq -in certs/ca.pem -signkey ca/ca_key.pem -out certreq.csr && \
    openssl ca -in certreq.csr -keyfile ca/ca_key.pem -days 3650 -out newcert.pem -config ./openssl.cnf &&\
    cp -r /etc/puppetlabs/puppet/ssl/ca/ca_crt.pem{,.bak} && \
    cp newcert.pem ca/ca_crt.pem && \
    rm /etc/puppetlabs/puppet/ssl/certs/ca.pem && \
    rm -rfv certreq.csr index.txt* newcert* serial.old && \
    puppet agent -t
    """)

if __name__ == "__main__":
    renew_ca_puppet()

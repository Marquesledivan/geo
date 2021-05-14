def revoked_certs(hosts):
    try:
        headers = {"Content-Type": "text/pson"}
        data = {"desired_state":"revoked"}
        payload = json.dumps(data)
        r = requests.put(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_status/{hosts}' \
        ,data=payload,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
        r = requests.delete(f'https://master.ledivan.com.br:8140/puppet-ca/v1/certificate_status/{hosts}' \
        ,data=payload,headers=headers,verify=False,cert=(f'{certs}master.ledivan.com.br.pem',"{}master.ledivan.com.br.pem".format(private_keys)))
    except json.decoder.JSONDecodeError as e:
        print(e)

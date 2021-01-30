# Puppet Node Purging via API

When you're decomissioning a machine that has been managed by Puppet you may want to programatically clean up the node. There are two parts to this:
- revoking and deleting the certificate of the node in Puppet's CA
- deactivating the node in PuppetDB

The following should work for Puppet 4.x and Puppet DB 4.x (including Puppet Enterprise 2016.4.x, 2017.1.x, 2017.2.x).

I've used certificate based auth, and the examples are being run from the puppet master so make use of existing certificates for authentication. When run remotely the cacert, certificate and corresponding private key for authentication will need to be present. 

## API References

* Certifiate Status: https://docs.puppet.com/puppet/4.10/http_api/http_certificate_status.html
* Using certificate auth with Puppet DB: https://docs.puppet.com/puppetdb/4.2/api/query/curl.html#using-a-certificateprivate-key-pair
* Puppet DB Node Deactivate command api: https://docs.puppet.com/puppetdb/4.2/api/command/v1/commands.html#deactivate-node-version-3 
* Deactivate wire format: https://docs.puppet.com/puppetdb/4.2/api/wire_format/deactivate_node_format_v3.html


## Example

I have a node foo.example that I have decomissioned and now I want to revoke and delete its certificate, and deactivate it in PuppetDB. 

Here's how it looks in PuppetDB:

```bash
[centos@pe-201620-master ~]$ curl http://localhost:8080/pdb/query/v4/nodes/foo.example | python -m json.tool
```

```json
{
    "cached_catalog_status": "not_used",
    "catalog_environment": "production",
    "catalog_timestamp": "2017-05-24T01:22:59.300Z",
    "certname": "foo.example",
    "deactivated": null,
    "expired": null,
    "facts_environment": "production",
    "facts_timestamp": "2017-05-24T01:22:58.768Z",
    "latest_report_corrective_change": true,
    "latest_report_hash": "70c2d9b0caf8b88d32870c84cca4e94733a1620e",
    "latest_report_noop": false,
    "latest_report_noop_pending": false,
    "latest_report_status": "failed",
    "report_environment": "production",
    "report_timestamp": "2017-05-24T01:22:57.764Z"
}
```

Here's how it looks in the CA:

```bash
[centos@pe-201620-master ~]$ sudo bash node_ca_status.sh | python -m json.tool
```

```json
{
    "dns_alt_names": [],
    "fingerprint": "3E:6F:77:5C:D1:8B:44:2D:FB:5F:0D:01:BE:E3:25:26:9A:C6:6F:D0:65:E6:FA:59:FE:D7:36:AA:DD:C9:93:70",
    "fingerprints": {
        "SHA1": "BD:60:05:EE:C3:13:99:59:29:F9:45:E8:DD:7F:06:34:D8:07:CF:00",
        "SHA256": "3E:6F:77:5C:D1:8B:44:2D:FB:5F:0D:01:BE:E3:25:26:9A:C6:6F:D0:65:E6:FA:59:FE:D7:36:AA:DD:C9:93:70",
        "SHA512": "9C:FA:3C:EE:86:15:43:E5:F3:51:23:DE:C4:F3:87:16:A7:C2:F6:62:F3:23:A3:AB:88:FE:B9:40:C2:22:56:BB:2C:48:CE:22:5E:06:CA:0D:EE:7D:43:08:AE:90:74:57:7F:DC:35:40:48:1B:D2:CA:F0:E3:C1:7E:C3:81:BF:62",
        "default": "3E:6F:77:5C:D1:8B:44:2D:FB:5F:0D:01:BE:E3:25:26:9A:C6:6F:D0:65:E6:FA:59:FE:D7:36:AA:DD:C9:93:70"
    },
    "name": "foo.example",
    "state": "signed"
}
```

## 1/ Revoke and Delete the certificate: 

```bash
sudo bash node_ca_revoke.sh
sudo bash node_ca_delete.sh
sudo bash node_ca_status.sh
Resource not found.
```

See attached shell scripts for curl commands used.

## 2/ Deactivate in PuppetDB

```bash
sudo bash node_deactivate.sh
```

puppetdb.log should then contain something like:

```
2017-05-24 01:59:06,229 INFO  [p.p.command] [763-1495591146220] [5 ms] 'deactivate node' command processed for foo.example
```

And now puppetdb query shows the node is deactivated:

```bash
[centos@pe-201620-master ~]$ sudo bash node_status.sh
```

```json
{
  "deactivated" : "2017-05-24T01:59:04.000Z",
  "latest_report_hash" : "d4e07ab3e9eeb14dcfc26b8aa90632adf6e5bcf2",
  "facts_environment" : "production",
  "cached_catalog_status" : "not_used",
  "report_environment" : "production",
  "latest_report_corrective_change" : true,
  "catalog_environment" : "production",
  "facts_timestamp" : "2017-05-24T01:44:28.618Z",
  "latest_report_noop" : false,
  "expired" : null,
  "latest_report_noop_pending" : false,
  "report_timestamp" : "2017-05-24T01:44:27.476Z",
  "certname" : "foo.example",
  "catalog_timestamp" : "2017-05-24T01:44:29.297Z",
  "latest_report_status" : "failed"
}
```

If you're running Puppet Enteprise, the node no longer appears under Inventory, but its reports are still available as they have not been purged. 



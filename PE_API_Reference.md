# Puppet Enterprise API's

Reference doc: <https://puppet.com/docs/pe/2017.3/overview/api_index.html>

## Authentication Methods

| API                                 | Endpoint                | RBAC Token         | Certificate        | How to whitelist a cert? |
|:------------------------------------|:------------------------|:------------------:|:------------------:|:-------------------------|
| [Activity](#activity)               | `/activity-api/v1/`     | :white_check_mark: | :white_check_mark: | `puppet_enterprise::profile::console::whitelisted_certnames`
| [Node Classifier](#node-classifier) | `/classifier-api/v1/`   | :white_check_mark: | :white_check_mark: | `puppet_enterprise::profile::console::whitelisted_certnames`
| [PuppetDB](#puppetdb)               | `/pdb/query/v4/`        | :white_check_mark: | :white_check_mark: | `puppet_enterprise::profile::puppetdb::whitelisted_certnames`
| [RBAC](#rbac)                       | `/rbac-api/v1/`         | :white_check_mark: | :white_check_mark: | `puppet_enterprise::profile::console::whitelisted_certnames`
| [Status](#status)<sup>1             | `/status/v1/`           | :white_check_mark: | :white_check_mark: | `puppet_enterprise::profile::console::whitelisted_certnames`
| [Code Manager](#code-manager)       | `/code-manager/v1/`     | :white_check_mark: | :x:                |
| [Orchestrator](#orchestrator)       | `/orchestrator/v1/`     | :white_check_mark: | :x:                | feature request: [ORCH-1679](https://tickets.puppetlabs.com/browse/ORCH-1679)
| [CA](#ca)                           | `/puppet-ca/v1/`        | :x:                | :white_check_mark: | `puppet_enterprise::profile::certificate_authority::client_whitelist`
| [Puppet Server](#puppet-server)     | `/puppet-admin-api/v1/` | :x:                | :white_check_mark: | [New auth.conf](https://puppet.com/docs/puppetserver/5.1/config_file_auth.html)<sup>2
| [Puppet](#puppet)                   | `/puppet/v3`            | :x:                | :white_check_mark: | [New auth.conf](https://puppet.com/docs/puppetserver/5.1/config_file_auth.html)<sup>2

<sup>1</sup> The Status API can be used without authentication.  
<sup>2</sup> auth.conf needs manually updated. [This module](https://forge.puppet.com/puppetlabs/puppet_authorization) can help automate that.  

Validated against Puppet Enterprise version **2017.3.5**

## Example Usage

### Activity

### CA

### Code Manager

### Node Classifier

### Orchestrator

<https://puppet.com/docs/pe/2017.3/orchestrator/orchestrator_api_v1_endpoints.html>

The Orchestrator API requires an RBAC token, and will not work with certificates. For a service account, generate a token that doesn't expire:

```
[root@pe-201735-agent ~]# puppet access login -l 0
Enter your Puppet Enterprise credentials.
Username: puppet_api_service_account
Password:

Access token saved to: /root/.puppetlabs/token
```

#### Run Puppet

Use either `puppet-job run` or the `/orchestrator/v1/command/deploy/` endpoint to trigger Puppet runs remotely.

>Note: User needs **"Run Puppet on agent nodes"** AND **"View node data from PuppetDB"** permissions to do this.

```
# Use a PQL query
puppet-job run -q 'facts {name = "osfamily" and value = "RedHat"}'

# Use a node list
puppet-job run -n "server1.foo.net,server2.foo.net"

# Run nodes against a feature branch with noop
puppet-job run -n "server1.foo.net,server2.foo.net" -e "fix_apache" --noop 
```

```
# Run puppet on a list of nodes
curl -sk https://puppet-master:8143/orchestrator/v1/command/deploy \
  -H "X-Authentication:$(puppet access show)" \
  -H "Content-Type: application/json" \
  -X POST \
  -d @- <<'EOF'
{
  "environment" : "production",
  "scope" : {
    "nodes" : [ "server1", "server2" ]
  }
}
EOF


# Run on all nodes in datacenter A, against a feature branch, with noop, and with concurrency.
curl -sk https://puppet-master:8143/orchestrator/v1/command/deploy \
  -H "X-Authentication:$(puppet access show)" \
  -H "Content-Type: application/json" \
  -X POST \
  -d @- <<'EOF'
{
  "environment" : "fix_apache",
  "noop" : true,
  "concurrency": 5,
  "scope" : {
    "query" : "facts { name = \"datacenter\" and value = \"A\" }"
  }
}
EOF
```

#### Run a Task

Use either `puppet-task run` or the `/orchestrator/v1/command/task/` endpoint to run a Puppet Task.

>Note: User needs **"Run Tasks"** and probably **"View node data from PuppetDB"** permissions to do this.

```
# Run a task with JSON parameters
puppet-task run service --params '{"action": "status", "name": "sshd"}' --nodes server1

# Run a task with arguments for parameters
puppet-task run service action=status name=sshd --nodes server1

# Run a task against nodes from a PQL query
puppet-task run service action=status name=sshd -q 'facts { name = "datacenter" and value = "A" }'
```

```
# Run a task on a set of nodes.
curl -sk https://puppet-master:8143/orchestrator/v1/command/task \
  -H "X-Authentication:$(puppet access show)" \
  -H "Content-Type: application/json" \
  -X POST \
  -d @- <<'EOF'
{
  "task" : "service",
  "params" : {
    "action" : "status",
    "name" : "sshd"
  },
  "scope" : {
    "nodes" : ["server1"]
  }
}
EOF

# Run a task from a non-production environment on nodes from a PQL query.
curl -sk https://puppet-master:8143/orchestrator/v1/command/task \
  -H "X-Authentication:$(puppet access show)" \
  -H "Content-Type: application/json" \
  -X POST \
  -d @- <<'EOF'
{
  "task" : "service",
  "environment": "try_something_new",
  "params" : {
    "action" : "status",
    "name" : "sshd"
  },
  "scope" : {
    "query" : "facts { name = \"datacenter\" and value = \"A\" }"
  }
}
EOF
```

#### View Jobs

Use either `puppet-job show` or the `/orchestrator/v1/jobs/` endpoint to view Orchestrator jobs.

>Note: User needs **"View Orchestrator"** permission to perform do this.

```
# View all jobs
puppet-job show

# View a job by numer
puppet-job show 3

# View a job with machine-readable JSON output
puppet-job show 3 --format json
```

```
# View all jobs
curl -sk -H "X-Authentication:$(puppet access show)" \
  https://puppet-master:8143/orchestrator/v1/jobs

# View a job by number (#3 in this case)
curl -sk -H "X-Authentication:$(puppet access show)" \
  https://puppet-master:8143/orchestrator/v1/jobs/3
```

### Puppet

### Puppet Server

### PuppetDB

Use either `puppet-query` or the `/pdb/query/v4/` endpoint to query PuppetDB.

>Note: User needs **"View node data from PuppetDB"** permission to use token-based authentication or whitelist a certificate and use cert-based authentication.

Reference Doc: <https://puppet.com/docs/puppetdb/5.1/api/index.html>  
PQL Reference Doc: <https://puppet.com/docs/puppetdb/5.1/api/query/tutorial-pql.html>  

`puppet-query` examples:

```
# Count all nodes per datacenter (based on a 'datacenter' fact).
puppet query 'facts[value, count(certname)] { name = "datacenter" group by value }'

# Show all the facts for a nodes matching a regular expression.
puppet query 'inventory[facts] { certname ~ foo }'

# Show all active nodes.
puppet query 'nodes {deactivated is null and expired is null}'
```

REST API examples:

```
# PQL (body data, POST): Count all nodes per datacenter (based on a 'datacenter' fact).
curl -sk https://puppet-master:8081/pdb/query/v4 \
  -X POST \
  -H 'Content-Type:application/json' \
  -H "X-Authentication:$(puppet access show)" \
  -d '{"query": "facts[value, count(certname)] { name = \"datacenter\" group by value }" }'


# PQL (urlencode data, GET): Count all nodes per datacenter (based on a 'datacenter' fact).
curl -sk https://puppet-master:8081/pdb/query/v4 \
  -X GET \
  -H "X-Authentication:$(puppet access show)" \
  --data-urlencode 'query=facts[value, count(certname)] { name = "datacenter" group by value }'

# AST (urlencode data, GET): Return the node object for the certname 'foo'.
curl -sk https://puppet-master:8081/pdb/query/v4 \
  -X GET \
  -H "X-Authentication:$(puppet access show)" \
  --data-urlencode 'query=["from","nodes",["=","certname","foo"]]'

# Use a whitelisted certificate instead of an RBAC token.
curl -sk https://puppet-master:8081/pdb/query/v4 \
  -X POST \
  -H 'Content-Type:application/json' \
  --cert   $(puppet config print hostcert) \
  --key    $(puppet config print hostprivkey) \
  --cacert $(puppet config print localcacert) \
  -d '{"query": "facts[value, count(certname)] { name = \"datacenter\" group by value }" }'
```

### RBAC

### Status

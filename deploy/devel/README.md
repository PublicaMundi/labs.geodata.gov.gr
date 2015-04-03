# Deploy for development #


## Requirements

### Required command-line utilities

We assume the following command-line utilities are available at Ansible's control machine: 

* wget
* jq

### Required files

A certain number of files should be provided at Ansible's control machine:

* an authorized-keys file to be used for normal users (if those are created). This is used
  by `node` role, and should be placed at `roles/node/files/etc/ssh/authorized_keys`.

### Required variables

A certain number of variables must also be provided at group/host level. Some of them are considered 
sensitive data and must be placed under `group_vars/<group-name>/secrets.yml` (not under source control):

 * `tomcat.manager.password` (under `group_vars/search-engine/secrets.yml`).
    This is a plain string value. The provided password will be assigned to a Tomcat user holding the 
    manager role (grants access to the manager gui).
 * `postgres.credentials` (under `group_vars/database/secrets.yml`).
    This is a list of dictionaries with keys of "username", "password". Provided credentials will be 
    assigned to existing PostgreSQL users (for normal logins).
 * `collectd.cgp.authn.credentials` (under `group_vars/monitor/secrets.yml`). 
    This is a list of dictionaries with keys of "username", "password". Provided credentials will be
    used to grant access to the CGP web application (via HTTP Digest Authentication) 

## Quickstart

Look at `deploy.sh` which runs several Ansible playbooks to perform a Publicamundi deployment.


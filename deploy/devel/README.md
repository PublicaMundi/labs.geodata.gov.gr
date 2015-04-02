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
* (_deprecated_) a file containing credentials (lines of user:password) for CGP web interface, which is used
  by `collectd-server` role abd should should be placed at `roles/collectd-server/files/etc/apache2/secrets`

### Required variables

A certain number of variables must also be provided at group/host level. Some of them are considered 
sensitive data and must be placed under `group_vars/<group-name>/secrets.yml` (not under source control):

 * `tomcat.manager.password` (under `group_vars/search-engine/secrets.yml`) 

## Quickstart

Look at `deploy.sh` which runs several Ansible playbooks to perform a Publicamundi deployment.


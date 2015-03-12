# Deploy for development #


## Requirements

### Required Bash utilities

We assume the following command-line utilities are available at Ansible's control machine: 
* wget
* jq

### Required files

Supply an authorized-keys file to be used for normal users (if those are created). This is used
by `node` role. and should be placed at `roles/node/files/etc/ssh/authorized_keys`.


## Quickstart

Look at `deploy.sh` which plays several Ansible playbooks to perform a Publicamundi deployment.



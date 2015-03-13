# Deploy for development #


## Requirements

### Required command-line utilities

We assume the following command-line utilities are available at Ansible's control machine: 

* wget
* jq

### Required files

A certain numner of files should be provided at Ansible's control machine:

* an authorized-keys file to be used for normal users (if those are created). This is used
  by `node` role, and should be placed at `roles/node/files/etc/ssh/authorized_keys`.
* a password for Tomcat's `tomcat` user which can access the manager (graphical) interface. 
  This used by `solrX` roles, and is placed at `roles/solrX/files/secrets/manager-password`. 

### Required variables

__Todo__

## Quickstart

Look at `deploy.sh` which runs several Ansible playbooks to perform a Publicamundi deployment.


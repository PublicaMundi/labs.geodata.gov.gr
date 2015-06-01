# Deploy for development #


## Basic Requirements

### Requirements for hosts

The minimal requirements for Ansible to execute tasks on a host machine (for now just Python) can be fullfilled with an Ansible adhoc command. For example, we can install them to all known hosts as below:

    ansible -m script -a install-ansible-prereqs.sh all

### Requirements for control host

We assume the following command-line utilities are available at Ansible's control machine: 

 * wget
 * jq
 * sshpass

## Playbooks

### Play: `prepare-deploy.yml`

This play is responsible to prepare the deployment locally (admin node). Basically, it downloads external files (e.g. Solr schema configuration) needed for roles, or computes site-global caches. Must be invoked just before `deploy.yml`. 

### Plays: `deploy-*.yml`

This is responsible to setup the _geodata.gov.gr_ PublicaMundi deployment.

#### Required files

A certain number of files should be provided at Ansible's control machine:

 * If `authorized_keys` or `private_keys` are supplied, the corresponding key files must exist under `files/keys`. See details in the dedicated README for the `cli` role.

## Quickstart

See `deploy.sh`.


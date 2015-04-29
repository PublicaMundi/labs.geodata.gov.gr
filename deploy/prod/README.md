# Deploy for production #


## Basic Requirements

### Requirements for hosts

The minimal requirements for Ansible to execute tasks on a host machine (for now just Python) can be fullfilled with an Ansible adhoc command. For example, we can install them to all known hosts that can be accessed externally (the group `external`) as below:

    ansible -m script -a install-ansible-prereqs.sh external

### Requirements for control hosts

We assume the following command-line utilities are available at Ansible's control machine: 

 * wget
 * jq
 * sshpass

## Playbooks

### Play: prepare-admin.yml

This play is responsible to prepare an administration node that will subsequently control the PublicaMundi deployment (for initial setup, updates etc.). After installing some minimal requirements, it will checkout this same repository.

### Play: setup-network.yml

This play is intended to be applied before main deployment of applications (play.yml). 
It has the following objectives:

 * Disable Debian's network-manager
 * Configure internal network (10.0.3.x)
 * Configure public interfaces (IPv6, IPv4 if exists) 
 * Setup SSH port forwardings from admin to internal hosts
 * Setup firewalls
 * Provide site-local aliases for hosts

If all the above are satisfied (e.g. networks are already setup manually be the administrator), this play can be omitted.

### Play: play.yml

This is the basic play responsible to setup the `geodata.gov.gr` PublicaMundi deployment.

#### Required files

A certain number of files should be provided at Ansible's control machine:

 * If `authorized_keys` or `private_keys` are supplied, the corresponding key files must exist under `files/keys`. See details in the dedicated README for the `cli` role.

#### Required variables

A certain number of variables must also be provided at group/host level. Some of them are considered sensitive data and must be placed under `group_vars/<group-name>/secrets.yml` (not under source control):

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

Take a look at `deploy.sh`.


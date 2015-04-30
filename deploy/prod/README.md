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

### Play: prepare-admin-workspace.yml

This play is controlled from *outside* of the target deployment, and is responsible to prepare an admin node (i.e. an Ansible control) that will subsequently control all the aspects of PublicaMundi deployment (for initial setup, updates etc.). 

After installing some minimal requirements, it will:
  * Setup a system-wide Python virtual environment
  * Setup a workspace
  * Checkout this repository into workspace

If all the above are satisfied, this play can be omitted.

### Play: prepare-admin-network.yml

This play is also controlled from *outside* of the target deployment, and is responsible to configure/setup the network infrastructure (on the admin node) needed for building an internal (site-local) network. Basically, it will:  

 * Disable Debian's network-manager
 * Configure internal network (10.0.3.0/24)
 * Configure public interfaces (IPv6, IPv4)
 * Generate /etc/hosts (site-local aliases for hosts)
 * Setup SSH forwardings from admin to internal hosts (and accompanying ssh-config stanzas for clients)
 * Setup firewall

If all the above are satisfied (e.g. networks are already setup manually be the administrator), this play can be omitted.

### Play: setup-network.yml

This play is controlled from the admin node (so, from *inside* of the target deployment), and is responsible for setting-up the internal network. For each host, it will:

 * Disable Debian's network-manager
 * Configure internal network (10.0.3.0/24)
 * Configure public interfaces (IPv6, IPv4 if exists) 
 * Generate /etc/hosts (site-local aliases for hosts)
 * Setup firewall

If all the above are satisfied (e.g. networks are already setup manually be the administrator), this play can be omitted.

### Play: deploy.yml

This play is controlled from the admin node, and is responsible to setup the `geodata.gov.gr` PublicaMundi deployment.

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

See `deploy.sh`.


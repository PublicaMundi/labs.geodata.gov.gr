#!/bin/bash

#
# Prepare needed stuff at control machine (i.e. localhost)
#

ansible-playbook -i hosts.conf --force-handlers -v prepare.yml

#
# Run playbooks for various groups (of managed hosts)
#

ansible-playbook -i hosts.conf -v -l monitor play.yml

ansible-playbook -i hosts.conf -v -l search-engine play.yml

ansible-playbook -i hosts.conf -v -l database play.yml

ansible-playbook -i hosts.conf -v -l catalog play.yml

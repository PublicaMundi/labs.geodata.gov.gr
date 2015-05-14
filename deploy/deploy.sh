#!/bin/bash

#
# Prepare needed stuff at control machine (i.e. localhost)
#

ansible-playbook --force-handlers -v prepare.yml

#
# Run playbooks for various groups (of managed hosts)
#

ansible-playbook -v -l monitor play.yml

ansible-playbook -v -l search-engine play.yml

ansible-playbook -v -l database play.yml

ansible-playbook -v -l catalog play.yml

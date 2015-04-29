#!/bin/bash


ansible -v -m script -a 'install-ansible-prereqs.sh' external-admin
if [ "$?" -ne "0" ]; then 
    echo "$0: Failed to install Ansible prerequisites"
    exit 1
fi

ansible-playbook -v prepare-admin-workspace.yml
if [ "$?" -ne "0" ]; then 
    echo "$0: Failed to execute playbook"
    exit 1
fi

ansible-playbook -v prepare-admin-network.yml
if [ "$?" -ne "0" ]; then 
    echo "$0: Failed to execute playbook"
    exit 1
fi

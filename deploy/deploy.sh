#!/bin/bash

DEPLOY=$0

function play()
{
    local playbook=${1}
    ansible-playbook -v ${playbook}
    if [ "$?" -ne "0" ]; then 
        echo "${DEPLOY}: Failed during playbook ${playbook}";
        exit 1
    fi
}

play 'deploy-all-boilerplate.yml'

play 'deploy-nfs.yml'

play 'deploy-database.yml'

play 'deploy-solr.yml'

play 'deploy-ckan.yml'

play 'deploy-geoserver.yml'

play 'deploy-proxy.yml'

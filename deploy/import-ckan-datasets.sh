#/bin/bash

## Options

host=admin.publicamundi.localdomain
port=8090
folder=files/groups/ckan/initialize/datasets/

## Main

screen_name=serve-folder-${RANDOM}

folder=$(cd ${folder} && pwd)

# Start HTTP server at datasets folder
screen -dm -S ${screen_name} scripts/serve-folder.py -p ${port} -l ${host} ${folder}

# Import datasets
ansible-playbook -v \
  -e web_folder=http://${host}:${port}/xml -e folder=${folder}/xml \
  scratch.yml

# Stop HTTP server
screen -S ${screen_name} -X quit

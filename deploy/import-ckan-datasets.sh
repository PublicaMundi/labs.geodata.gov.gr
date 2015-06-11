#/bin/bash

host=admin.publicamundi.localdomain
port=8090
datasets_folder=files/groups/ckan/initialize/datasets/

screen_name=serve-folder-${RANDOM}

# Start HTTP server at datasets folder

screen -dm -S ${screen_name} scripts/serve-folder.py -p ${port} -l ${host} ${datasets_folder}

# Import datasets

ansible-playbook -v -e datasets_folder=http://${host}:${port}/xml scratch.yml

# Stop HTTP server

screen -S ${screen_name} -X quit
#echo 'Stopped screen: ' ${screen_name}

#/bin/bash

FOLDER=files/groups/ckan/initialize/datasets/

# Set defaults, read options

step=
skip_tags=
host=admin.publicamundi.localdomain
port=8090

while getopts "1hs:l:p:" opt; do
    case $opt in
        1) 
            step=1
            ;;
        s)
            skip_tags=${OPTARG}
            ;;
        l)
            host=${OPTARG}
            ;;
        p)  
            port=${OPTARG}
            ;;
        h)
            echo "Usage: ${0} [-1] [-s SKIP_TAGS] [-p PORT] [-h HOST]"
            exit 0
            ;;
        :)
            echo "Error: option ${OPTARG} requires an argument" 
            ;;
        ?)
            echo "Invalid option: ${OPTARG}"
            ;;
    esac
done

screen_name=serve-folder-${RANDOM}

folder=$(cd ${FOLDER} && pwd)

# Start HTTP server at datasets folder

screen -dm -S ${screen_name} scripts/serve-folder.py -p ${port} -l ${host} ${folder}

# Import datasets

pb_opts="-v"
[ -n "${skip_tags}" ] && pb_opts="${pb_opts} --skip-tags ${skip_tags}"
[ -n "${step}" ] && pb_opts="${pb_opts} --step"

ansible-playbook ${pb_opts} -e web_folder=http://${host}:${port}/xml -e folder=${folder}/xml import-ckan-datasets.yml

# Stop HTTP server

screen -S ${screen_name} -X quit

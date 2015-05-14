#!/bin/sh
if [ ! -f /root/.ansible_prereqs_installed ]; then
        apt-get update
        apt-get install -y python python-apt python-pycurl sshpass
        touch /root/.ansible_prereqs_installed
        echo "CHANGE"
fi

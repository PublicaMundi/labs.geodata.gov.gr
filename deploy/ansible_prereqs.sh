#!/bin/sh
rm /etc/apt/sources.list
cat << EOF > "/etc/apt/sources.list"
deb http://ftp.gr.debian.org/debian/ wheezy main
deb-src http://ftp.gr.debian.org/debian/ wheezy main
deb http://security.debian.org/ wheezy/updates main
deb-src http://security.debian.org/ wheezy/updates main
deb http://ftp.gr.debian.org/debian/ wheezy-updates main
deb-src http://ftp.gr.debian.org/debian/ wheezy-updates main
EOF

if [ ! -f /root/.ansible_prereqs_installed ]; then
        apt-get update
        apt-get install -y python python-apt python-pycurl sshpass
        touch /root/.ansible_prereqs_installed
        echo "CHANGE"
fi

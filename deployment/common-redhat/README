Installing geodata.gov.gr 
=========================

Install ansible on your local machine (probably ok to do this globally)

pip install ansible

Have a bare Redhat 6 or CentOS 6 box that you have ssh login too.

Make a hosts file /etc/ansible/hosts containing the IP of the server you want to deploy to

```
[dev]
192.168.x.x
```

Run the ansible playbook

ansible-playbook geodatagovgr_dev.yml

You may have to supply connection parameters to ansible-playbook i.e private-key or password to connect.  See ansible-playbook --help

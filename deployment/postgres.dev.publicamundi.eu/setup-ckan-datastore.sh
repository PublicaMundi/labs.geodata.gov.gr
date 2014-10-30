#!/bin/bash

script=$(pwd)/setup-ckan-datastore/datastore_setup.py

# We want set_permissions.sql to be accessible by user "postgres", so we copy
# it somewhere public

cp -v $(pwd)/setup-ckan-datastore/set_permissions.sql /tmp/set_permissions.sql
cd /tmp

# Sudo as postgres and grant permissions ...

python ${script} -p postgres ckan ckan_data ckaner ckan_datastorer ckaner

# Cleanup

rm -v set_permissions.sql


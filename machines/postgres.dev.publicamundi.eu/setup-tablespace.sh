#!/bin/bash

tablespace='/var/local/lib/postgresql/tablespace-1'

mkdir -p ${tablespace}

chown -R postgres:postgres ${tablespace}

sudo -u postgres psql -e -c "CREATE TABLESPACE tablespace_1 LOCATION '${tablespace}'"


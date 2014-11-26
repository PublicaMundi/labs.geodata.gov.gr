#!/bin/bash

sudo -u postgres createdb -e -D pg_default -E utf8 template_postgis
sudo -u postgres psql template_postgis \
   -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
sudo -u postgres psql template_postgis \
   -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql

# Create databases

sudo -u postgres createdb -e -O ckaner -D tablespace_1 -E utf8 -T template_postgis ckan
sudo -u postgres createdb -e -O ckaner -D pg_default -E utf8 -T template_postgis ckan_tests
sudo -u postgres createdb -e -O ckan_datastorer -D tablespace_1 -T template_postgis -E utf8 ckan_data
sudo -u postgres createdb -e -O ckan_datastorer -D pg_default -E utf8 ckan_data_tests

sudo -u postgres createdb -e -O rasdaman -D tablespace_1 -E utf8 rasdaman
sudo -u postgres createdb -e -O petascope -D tablespace_1 -E utf8 petascope

# Grant permissions to geometry tables

for db in "ckan" "ckan_data" "ckan_tests"; do
   sudo -u postgres psql ${db} -c 'ALTER TABLE spatial_ref_sys OWNER TO ckaner'
   sudo -u postgres psql ${db} -c 'ALTER TABLE geometry_columns OWNER TO ckaner'
done

# Grant view permissions to geoserver on CKAN datastore
# Note: Maybe this should run after setup-datastore.sh ??

sudo -u postgres psql ckan_data -c \
    'GRANT ALL ON SCHEMA public TO geoserver'
sudo -u postgres psql ckan_data -c \
    'GRANT SELECT ON ALL TABLES IN SCHEMA public TO geoserver'
sudo -u postgres psql ckan_data -c \
    'ALTER DEFAULT PRIVILEGES FOR ROLE ckan_datastorer IN SCHEMA public GRANT SELECT ON TABLES TO geoserver'


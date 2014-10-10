#!/bin/bash

sudo -u postgres createdb -e -D pg_default -E utf8 template_postgis
sudo -u postgres psql template_postgis \
   -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
sudo -u postgres psql template_postgis \
   -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql

sudo -u postgres createdb -e -O ckaner -D tablespace_1 -E utf8 -T template_postgis ckan
sudo -u postgres createdb -e -O ckaner -D pg_default -E utf8 -T template_postgis ckan_tests
sudo -u postgres createdb -e -O ckan_datastorer -D tablespace_1 -E utf8 ckan_data
sudo -u postgres createdb -e -O ckan_datastorer -D pg_default -E utf8 ckan_data_tests

sudo -u postgres createdb -e -O rasdaman -D tablespace_1 -E utf8 rasdaman


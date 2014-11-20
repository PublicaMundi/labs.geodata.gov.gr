#!/bin/bash

sudo -u postgres createuser -e -l -D ckaner
sudo -u postgres createuser -e -l -D ckan_datastorer

sudo -u postgres createuser -e -l -D geoserver

sudo -u postgres createuser -e -l -D rasdaman
sudo -u postgres createuser -e -l -D petascope


#!/bin/bash

# Retreive repo's public key and trust it
wget --no-check-certificate --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Append config stanza for APT sources 
cat >>/etc/apt/sources.list <<EOD

# wheezy-pgdg, PostgreSQL apt repos
deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main

EOD

# Update package lists
apt-get update

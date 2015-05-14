#!/bin/bash

if [ ! -f ~/.ansible-prereqs-installed ]; then
   apt-get install -y python
   [ "$?" -eq 0 ] && touch ~/.ansible-prereqs-installed
fi

#!/bin/bash

if [ ! -d "${CKAN_PYENV}" ]; then
    echo 'CKAN_PYENV is not a directory!'
    exit 1
fi

if [ ! -x "${CKAN_PYENV}/bin/python" ]; then
    echo 'CKAN_PYENV does not seem like a virtual environment!'
    exit 1
fi

cd ${CKAN_PYENV}/src

# Merge PO files
msgcat -o /tmp/ckan.po ckanext-publicamundi/i18n/el/LC_MESSAGES/ckanext-publicamundi.po  ckan/ckan/i18n/el/LC_MESSAGES/ckan.po
if [ "$?" -ne 0 ]; then
    echo 'Failed to merge PO files: aborting'
    exit 1
fi

# Compile to a single MO file
msgfmt -o /tmp/ckan.mo /tmp/ckan.po
if [ "$?" -ne 0 ]; then
    echo 'Failed to compile PO file'
    exit 1
fi

# Replace existing messages
mv -v /tmp/ckan.mo ckan/ckan/i18n/el/LC_MESSAGES/ckan.mo

echo "Compiled PO messages under $(cd ckan/ckan/i18n/el/LC_MESSAGES && pwd)/ckan.mo"
echo 'Now, restart the web server!'


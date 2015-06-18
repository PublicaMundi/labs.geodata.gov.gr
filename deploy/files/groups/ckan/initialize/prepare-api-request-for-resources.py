#!/usr/bin/env python

import csv
import os
import json
import argparse
import logging
import hashlib

logging.basicConfig(level=logging.INFO)

argp = argparse.ArgumentParser()
argp.add_argument("inputs", metavar='INFILE', type=str, nargs=1)
argp.add_argument("-b", "--resources-folder", dest='resources_folder', 
    default='resources', help=u'The base directory for resource files') 

def prepare_json_requests(infile, resources_folder):
    res = []
    
    with open(infile, 'r') as ifp:
        i = 0
        reader = csv.DictReader(ifp)
        for item in reader:
            i = i + 1
            package_id = item['dataset_uid'].decode('ascii')
            
            resource_name = item['resource_machine_name'].decode('ascii')
            resource_title = item['resource_name'].decode('utf-8')
            resource_type = item['resource_type'].decode('ascii')
            
            category = item['category']
            
            relpath = item['location'].decode('ascii')
            resource_path = os.path.realpath(os.path.join(resources_folder, relpath))
            if not os.path.isfile(resource_path):
                logging.error('A resource file is missing: categ=%s relpath=%s', 
                    category, relpath)
                continue
            
            hexdigest = None
            with open(resource_path, 'r') as ifp:
                hexdigest = hashlib.sha1(ifp.read()).hexdigest()
        
            req_data = {
                'package_id': package_id,
                'format': resource_type,
                'name': resource_title,
                'hash': hexdigest,
                'upload': resource_path,
            }
            res.append(req_data)

    print json.dumps(res)

if __name__ == '__main__':
    args = argp.parse_args()
    prepare_json_requests(args.inputs[0], args.resources_folder)


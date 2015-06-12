#!/usr/bin/env python

import csv
import os
import json
import argparse
import logging

logging.basicConfig(level=logging.INFO)

OUTPUT_BASE_DIR = 'out'

argp = argparse.ArgumentParser()
argp.add_argument("inputs", metavar='INFILE', type=str, nargs=1)
argp.add_argument("--rename", dest='rename', default=False, action='store_true',
    help=u'Allow renaming of datasets') 
argp.add_argument("--web-folder", dest='web_folder', type=str, 
    default='http://localhost:8080', 
    help=u'The web folder under which source metadata files will be served')

def prepare_json_requests(infile, web_folder, rename=False):
    res = []
    
    output_dir = os.path.join(OUTPUT_BASE_DIR, 'json', 'datasets')
    try:
       os.makedirs(output_dir)
    except OSError as ex:
        if not ex.errno == os.errno.EEXIST:
            raise ex
    
    logging.info('Using output directory at %s' %(output_dir))
    with open(infile, 'r') as ifp:
        i = 0
        reader = csv.DictReader(ifp)
        for item in reader:
            i = i + 1
            dataset_id = item['dataset_id']
            owner_org = item['organization_name']
            outfile = os.path.join(output_dir, '%s.json' %(dataset_id))
            with open(outfile, 'w') as ofp:
                req = {
                    'dtype': 'inspire',
                    'source': '%s/%s.xml' %(web_folder, dataset_id),
                    'owner_org': owner_org,
                    'rename_if_conflict': rename,
                    'continue_on_errors': False
                }
                ofp.write(json.dumps(req))
            res.append(dict(name=dataset_id, path=os.path.realpath(outfile)))

    print json.dumps(res)

if __name__ == '__main__':
    args = argp.parse_args()
    prepare_json_requests(args.inputs[0], args.web_folder, args.rename)


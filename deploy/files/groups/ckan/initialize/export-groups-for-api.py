#!/usr/bin/env python

import sys
import csv
import os
import json
import urllib2
import urllib
import pprint
from unidecode import unidecode
import logging

INPUT = sys.argv[1]
OUTPUT_BASE_DIR = 'out'

URL_BASE = 'http://ckan.example.com:5000'
API_KEY = 'XXX'

logging.basicConfig(level=logging.INFO)

input_name = os.path.splitext(os.path.basename(INPUT))[0]

def csv_to_json():
    res = {
        'groups': {}
    }

    output_dir = os.path.join(OUTPUT_BASE_DIR, 'json', input_name)
    try:
       os.makedirs(output_dir)
    except OSError as ex:
        if not ex.errno == os.errno.EEXIST:
            raise ex
    
    logging.info('Using output directory at %s' %(output_dir))

    with open(INPUT, 'r') as ifp:
        i = 0
        reader = csv.DictReader(ifp)
        for item in reader:
            i = i + 1
            name = item['name']
            if not name: 
                logging.error('Found an empty name (record %d, at line %d): Skipping' %(
                    i, reader.line_num))
                continue
            else:
                logging.info('Reading fields for group: %s' %(name))
            title_el = item['title_el'].decode('utf-8')
            title_en =  item['title_en'].decode('utf-8')
            description_el = item['description_el'].decode('utf-8')
            description_en = item['description_en'].decode('utf-8')
            image_url = item['logo_url']

            org_dict = {
               'name': name,
               'title': title_en if title_en else title_el,
               'description': description_en if description_en else description_el,
               'image_url': image_url,
            }

            translate_dict = {'data': []}
            
            if description_en:
                translate_dict['data'].append({
                    'term': description_en,
                    'term_translation': description_el,
                    'lang_code': 'el'
                })

            if title_en:
                translate_dict['data'].append({
                    'term': title_en,
                    'term_translation': title_el,
                    'lang_code': 'el'
                })
            

            res['groups'][name] = {}

            outfile = os.path.join(output_dir, '%s.json' %(name))
            with open(outfile, 'w') as ofp:
                ofp.write(json.dumps(org_dict))
            res['groups'][name]['create'] = os.path.realpath(outfile)
            
            if translate_dict['data']:
                # Create only if at least 1 actual translation exists
                outfile = os.path.join(output_dir, 'translate-%s.json' %(name)) 
                with open(outfile, 'w') as ofp:
                    ofp.write(json.dumps(translate_dict))
                res['groups'][name]['translate'] = os.path.realpath(outfile)
            else:
                logging.warn('Skipping translation for group (%s): %s' % (input_name, name))
        
        # Done
        print json.dumps(res, indent=4)

def make_api_call(org_dict, api_action):
    '''
    Examples:
    >>> make_api_call(group_dict, 'group_create')
    >>> make_api_call(org_dict, 'organization_create')
    >>> make_api_call(translate_dict, 'term_translation_update_many')
    '''
    # use the json module to dump the dictionary to a string for posting.
    data_string = urllib.quote(json.dumps(org_dict))
    # we'll use the package_create function to create a new dataset.
    url = URL_BASE + '/api/action/' + api_action
    #print org_dict.get('name')
    request = urllib2.Request(url)

    request.add_header('authorization', API_KEY)
    try:
        # make the http request.
        response = urllib2.urlopen(request, data_string)
        print 'response:'
        print response
        assert response.code == 200
        # use the json module to load ckan's response into a dictionary.
        response_dict = json.loads(response.read())
        assert response_dict['success'] is True

        # package_create returns the created package as its result.
        created_package = response_dict['result']
        pprint.pprint(created_package)
    except:
        pass

if __name__ == '__main__':
    csv_to_json()


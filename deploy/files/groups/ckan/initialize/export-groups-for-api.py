#!/usr/bin/env python

import csv
import os
import json
import urllib2
import urllib
import pprint
import argparse
import logging

#logging.basicConfig(level=logging.INFO)

OUTPUT_BASE_DIR = 'out'

URL_BASE = 'http://ckan.example.com:5000'
API_KEY = 'XXX'

argp = argparse.ArgumentParser()
argp.add_argument("inputs", metavar='INFILE', type=str, nargs=1)
argp.add_argument("--translate", dest='translate', default=False, action='store_true')

def csv_to_json(infile, translate=False):
    res = []
    
    input_name = os.path.splitext(os.path.basename(infile))[0]
    output_dir = os.path.join(OUTPUT_BASE_DIR, 'json', input_name)
    
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
            
            name = item['name']
            assert name, 'Found an empty name (record %d, at line %d)' %(i, reader.line_num)
            logging.info('Reading fields for group: %s' %(name))
            
            title_el = item['title_el'].decode('utf-8')
            title_en =  item['title_en'].decode('utf-8')
            description_el = item['description_el'].decode('utf-8')
            description_en = item['description_en'].decode('utf-8')
            image_url = item['logo_url'].decode('ascii', errors='ignore')

            if not translate:
                # Print the path for JSON that creates group
                org_dict = {
                    'name': name,
                    'title': title_en if title_en else title_el,
                    'description': description_en if description_en else description_el,
                    'image_url': image_url,
                }
                outfile = os.path.join(output_dir, '%s.json' %(name))
                with open(outfile, 'w') as ofp:
                    ofp.write(json.dumps(org_dict))
                res.append(dict(name=name, path=os.path.realpath(outfile)))
            else:
                # Print the path for JSON that translates group title/description
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
                if translate_dict['data']:
                    # Create only if at least 1 actual translation exists
                    outfile = os.path.join(output_dir, 'translate-%s.json' %(name)) 
                    with open(outfile, 'w') as ofp:
                        ofp.write(json.dumps(translate_dict))
                    res.append(dict(name=name, path=os.path.realpath(outfile)))
                else:
                    logging.warn('Skipping translation for group (%s): %s' % (input_name, name))
    # Done
    print json.dumps(res)

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
    args = argp.parse_args()
    csv_to_json(args.inputs[0], args.translate)



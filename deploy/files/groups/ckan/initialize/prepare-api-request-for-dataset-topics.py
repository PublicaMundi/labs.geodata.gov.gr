#!/usr/bin/env python

import csv
import os
import json
import argparse
import logging
from lxml import etree
from uuid import UUID
from inflection import (dasherize, underscore)

logging.basicConfig(level=logging.INFO)

OUTPUT_BASE_DIR = 'out'

argp = argparse.ArgumentParser()
argp.add_argument('topics_file', metavar='TOPICS_FILE', nargs=1)
argp.add_argument('datasets_file', metavar='DATASETS_FILE', nargs=1)
argp.add_argument('-f', '--folder', dest='datasets_folder', 
    default='datasets/xml')

namespaces = {
    'gmd': 'http://www.isotc211.org/2005/gmd',
    'gco': 'http://www.isotc211.org/2005/gco',
    'gml': 'http://www.opengis.net/gml',
}

def prepare_json_requests(topic_names, identifiers, datasets_folder):
    res = []
    
    output_dir = os.path.join(OUTPUT_BASE_DIR, 'json', 'dataset-topics')
    try:
       os.makedirs(output_dir)
    except OSError as ex:
        if not ex.errno == os.errno.EEXIST:
            raise ex
    
    logging.info('Using output directory at %s' %(output_dir))
    
    munge = lambda name: dasherize(underscore(name))
    
    for identifier in identifiers:
        md_file = os.path.join(datasets_folder, '%s.xml' % (identifier))
        md = etree.parse(md_file)
        q_identifier = md.xpath(
            '/gmd:MD_Metadata' +
                '/gmd:identificationInfo/gmd:MD_DataIdentification' + 
                    '/gmd:citation/gmd:CI_Citation' +
                        '/gmd:identifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
            namespaces=namespaces)
        assert len(q_identifier) == 1
        assert q_identifier[0].text == str(identifier), 'Found an unexpected identifier!' 
        q_topic = md.xpath(
            '/gmd:MD_Metadata' + 
                '/gmd:identificationInfo/gmd:MD_DataIdentification' + 
                    '/gmd:topicCategory/gmd:MD_TopicCategoryCode',
            namespaces=namespaces)
        for i, r in enumerate(q_topic):
            code = r.text
            name = munge(code)
            if not name in topic_names:
                logging.warn('Cannot map topic code %r to a topic group' % (code))
                continue
            # Prepare a member_create api request
            req = {
                'id': name, # group's name-or-id
                'object': str(identifier),
                'object_type': 'package',
                'capacity': 'public',
            }
            outfile = os.path.join(output_dir, '%s-topic-%d.json' %(identifier, i))
            with open(outfile, 'w') as ofp:
                ofp.write(json.dumps(req))
            res.append(dict(path=os.path.realpath(outfile)))
            
    print json.dumps(res)

if __name__ == '__main__':
    args = argp.parse_args()
    
    assert os.path.isdir(args.datasets_folder)
    
    topics_file = args.topics_file[0]
    with open(topics_file, 'r') as ifp:
        reader = csv.DictReader(ifp)
        topic_names = set([rec['name'] for rec in reader])
    
    datasets_file = args.datasets_file[0]
    with open(datasets_file, 'r') as ifp:
        reader = csv.DictReader(ifp)
        identifiers = set([UUID(rec['dataset_id']) for rec in reader])
    
    prepare_json_requests(topic_names, identifiers, args.datasets_folder)


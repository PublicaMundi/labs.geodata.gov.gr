#!/usr/bin/env python

from wsgiref.simple_server import make_server
import pycurl
import json
import logging

PORT = 8000

BACKEND_RELOAD_URL = 'http://%(host)s/geoserver/rest/reload'
NUM_BACKEND_SERVERS = {{geoserver.servers| length}}
BACKEND_SERVER_PORT_0 = 8081

USERPWD = 'admin:geoserver'

logging.basicConfig(level=logging.INFO)

def application(environ, start_response):

    # Iterate on backend servers and force them reload

    result = {}
    details = {}
    success = True
    for i in range(0, NUM_BACKEND_SERVERS):
        name = 'backend-%d' %(i + 1) 
        host = 'localhost:%d' % (BACKEND_SERVER_PORT_0 + i)
        # Prepare a cURL request
        c = pycurl.Curl()
        c.setopt(pycurl.URL,  BACKEND_RELOAD_URL % dict(host=host))
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.USERPWD, USERPWD)
        c.setopt(pycurl.POSTFIELDS, '')
        # Perform, trap errors
        try:
            c.perform()
            response_code = int(c.getinfo(c.RESPONSE_CODE))
            if response_code != 200:
                success = False
                details[name] = dict(message='Failed (HTTP %d)' % (response_code))
                logging.error('Failed to reload server at %s: %s', host, details[name])
            else:
                logging.info('Successfully reloaded server at %s', host)
        except pycurl.error as ex:
            success = False
            details[name] = dict(message='Failed (pycurl %d: %s)' % (ex.args))
    
    # Build a Celery-compliant webhook response with an overall status

    if success:
        result['status'] = 'success'
        result['retval'] = None
    else:
        result['status'] = 'failure'
        result['reason'] = 'Failed to reload backend servers'
        result['details'] = details

    start_response('200 OK', [('Content-type', 'application/json')])
    return [json.dumps(result)]

httpd = make_server('', PORT, application)
print "Serving HTTP on port %d..." %(PORT)
httpd.serve_forever()


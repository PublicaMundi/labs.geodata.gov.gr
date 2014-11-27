from wsgiref.simple_server import make_server
import pycurl
import json

PORT = 8000

BACKEND_RELOAD_URL = 'http://%(host)s/geoserver/rest/reload'
NUM_BACKEND_SERVERS = 4
FRONTEND_SERVER_PORT = 8080

USERPWD = 'admin:password'

def application(environ, start_response):
    
    # Iterate on backend servers and force them reload

    result = {}
    details = {}
    success = True
    for i in range(1, NUM_BACKEND_SERVERS + 1):
        name = 'backend-%d' %(i) 
        host = 'localhost:%d' % (FRONTEND_SERVER_PORT + i)
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


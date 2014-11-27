from wsgiref.simple_server import make_server
import pycurl
import json

NUM_BACKEND_SERVERS = 5

def application(environ, start_response):
    global NUM_BACKEND_SERVERS

    result = {}
    data = ''
    for i in range(1, NUM_BACKEND_SERVERS):
        c = pycurl.Curl()
        host = "localhost:%d" % (8080 + i)
        c.setopt(pycurl.URL, "http://%s/geoserver/rest/reload" % (host))
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.USERPWD, 'admin:password')
        c.setopt(pycurl.POSTFIELDS, data)
        try:
            c.perform()
            response_code = int(c.getinfo(c.RESPONSE_CODE))
            if response_code != 200:
                result[i] = dict(success=False, message='Failed (HTTP %d)' % (response_code))
            else:
                result[i] = dict(success=True)
        except pycurl.error as ex:
            result[i] = dict(
                success=False, message='Failed (pycurl %d: %s)' % (ex.args))
    start_response('200 OK', [('Content-type', 'application/json')])
    return [json.dumps(result)]

httpd = make_server('', 8000, application)
print "Serving HTTP on port 8000..."
httpd.serve_forever()


from wsgiref.simple_server import make_server
import pycurl
import json

def application(environ, start_response):
    result = {}
    data = ''
    for i in range(1,5):
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
                result[host] = 'Failed (HTTP %d)' % (response_code)
            else:
                result[host] = 'Ok'
        except Exception as ex:
            result[host] = 'Failed (%s)' % (ex)
    start_response('200 OK', [('Content-type', 'application/json')])
    return [json.dumps(result)]

httpd = make_server('', 8000, application)
print "Serving HTTP on port 8000..."
httpd.serve_forever()


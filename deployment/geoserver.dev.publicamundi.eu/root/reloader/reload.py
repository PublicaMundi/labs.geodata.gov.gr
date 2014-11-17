from wsgiref.simple_server import make_server, demo_app
import pycurl

def application(environ, start_response):
    for i in range(1,5):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "http://localhost:808" + str(i) + "/geoserver/rest/reload")
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.USERPWD, 'admin:password')
        c.perform()
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ["GeoServer reloaded"]

httpd = make_server('', 8000, application)
print "Serving HTTP on port 8000..."
httpd.serve_forever()


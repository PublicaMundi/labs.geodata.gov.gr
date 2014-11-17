# WSGI module for use with Apache mod_wsgi or gunicorn

from mapproxy.wsgiapp import make_wsgi_app
application = make_wsgi_app(r'/var/local/mapproxy/etc/mapproxy.yaml')

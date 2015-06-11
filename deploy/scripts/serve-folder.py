#!/usr/bin/env python

import argparse
import logging
import os
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

argp = argparse.ArgumentParser()
argp.add_argument('document_root', nargs=1, metavar='DOCUMENT_ROOT')
argp.add_argument("-l", dest='listen_address', default='127.0.0.1');
argp.add_argument("-p", dest='port', type=int, default=8000);

logging.basicConfig(level=logging.INFO)

def serve(address, document_root):
   os.chdir(document_root)
   logging.info('Using document-root: %s', document_root)
   httpd = HTTPServer(address, SimpleHTTPRequestHandler)
   sa = httpd.socket.getsockname()
   logging.info("Serving HTTP on %s:%s ..." %(sa[0], sa[1]))
   httpd.serve_forever()

if __name__ == "__main__":
   args = argp.parse_args()
   document_root = os.path.realpath(args.document_root[0])
   serve(address=(args.listen_address, args.port), document_root=document_root)

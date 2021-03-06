#!/usr/bin/python

import tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from urls import *
import argparse
import logging
from utils.Log import Log


parser = argparse.ArgumentParser()

parser.add_argument('--dev', action="store_true", default=False)

app.config['PROPAGATE_EXCEPTIONS'] = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    arguments = parser.parse_args()
    if arguments.dev:
        app.config['DEBUG'] = True
        Log.info("Running webserver in DEBUG mode")
        app.run(host = app.config['WEBSERVER_ADDR'], port = app.config['WEBSERVER_PORT'])
    else:
        Log.info("Running webserver in DEPLOYMENT mode")
        sockets = tornado.netutil.bind_sockets(app.config['WEBSERVER_PORT'])
        tornado.process.fork_processes(app.config['SUBPROCESS_NUMBER'])
        server = HTTPServer(WSGIContainer(app))
        server.add_sockets(sockets)
        IOLoop.current().start()

# -*- coding: utf-8 -*-
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Sylvain Hellegouarch nor the names of his
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__author__ = "Sylvain Hellegouarch"
__version__ = "0.1.0"
__doc__ = """
Module to host a Django application from within a CherryPy server.

Instead of creating a clone to `runserver` like other similar
packages do, we simply setup and host the Django application
using WSGI and CherryPy's capabilities to serve it.

In order to configure the application, we use the `settings.configure(...)`
function provided by Django.

Finally, since the CherryPy WSGI server doesn't offer a log
facility, we add a straightforward WSGI middleware to do so, based
on the CherryPy built-in logger. Obviously any other log middleware
can be used instead.
"""

# Python stdlib imports
import sys
import logging
import os, os.path

# Third-party imports
import cherrypy
from cherrypy.process import wspbus, plugins
from cherrypy import _cplogging, _cperror
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.http import HttpResponseServerError
import webbrowser
from bs4 import BeautifulSoup

from tango_project import settings

class Server(object):
    def __init__(self):
        self.base_dir = os.path.join(os.path.abspath(os.getcwd()), "tango_project")
		
        conf = {
             'server.socket_host': "127.0.0.1",
             'server.socket_port': 8000,
             'server.thread_pool': 10,
             'checker.on': False,
             'engine.autoreload_on': False,
             'log.screen': True,
             'log.error_file': "error.log",
             'log.access_file': "access.log",
			 }

        #conf_path = os.path.join(self.base_dir, "..", "server.cfg")
        cherrypy.config.update(conf)

        # This registers a plugin to handle the Django app
        # with the CherryPy engine, meaning the app will
        # play nicely with the process bus that is the engine.
        DjangoAppPlugin(cherrypy.engine, self.base_dir).subscribe()
		
    def browse(self):
        webbrowser.open_new("http://127.0.0.1:8000/rango")
    def run(self):
        engine = cherrypy.engine
        engine.signal_handler.subscribe()

        if hasattr(engine, "console_control_handler"):
            engine.console_control_handler.subscribe()
        cherrypy.engine.subscribe('engine.start', Server.browse(self), priority=90)
        engine.start()
        
        engine.block()

class DjangoAppPlugin(plugins.SimplePlugin):
    def __init__(self, bus, base_dir):
        """
        CherryPy engine plugin to configure and mount
        the Django application onto the CherryPy server.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.base_dir = base_dir

    def start(self):
        self.bus.log("Configuring the Django application")

        # Well this isn't quite as clean as I'd like so
        # feel free to suggest something more appropriate
        from tango_project.settings import *
        from django.conf import settings
        import django.contrib.sessions.serializers
        
        
		
        
        app_settings = locals().copy()
        del app_settings['self']
        settings.configure(**app_settings)
        import django.db.backends.sqlite3.base
		
        
        self.bus.log("Mounting the Django application")
        cherrypy.tree.graft(HTTPLogger(WSGIHandler()))

        self.bus.log("Setting up the static directory to be served")
        # We server static files through CherryPy directly
        # bypassing entirely Django
        staticpath = os.path.abspath(self.base_dir)
        staticpath = os.path.split(staticpath)[0]
        staticpath = os.path.join(staticpath, 'static')
		
        static_handler = cherrypy.tools.staticdir.handler(section="/", dir=staticpath, root='')
		
        cherrypy.tree.mount(static_handler, '/static')
    
class HTTPLogger(_cplogging.LogManager):
    def __init__(self, app):
        _cplogging.LogManager.__init__(self, id(self), cherrypy.log.logger_root)
        self.app = app
        
    def __call__(self, environ, start_response):
        """
        Called as part of the WSGI stack to log the incoming request
        and its response using the common log format. If an error bubbles up
        to this middleware, we log it as such.
        """
        try:
            response = self.app(environ, start_response)
            self.access(environ, response)
            return response
        except:
            self.error(traceback=True)
            return HttpResponseServerError(_cperror.format_exc())
        
    def access(self, environ, response):
        """
        Special method that logs a request following the common
        log format. This is mostly taken from CherryPy and adapted
        to the WSGI's style of passing information.
        """
        atoms = {'h': environ.get('REMOTE_ADDR', ''),
                 'l': '-',
                 'u': "-",
                 't': self.time(),
                 'r': "%s %s %s" % (environ['REQUEST_METHOD'], environ['REQUEST_URI'], environ['SERVER_PROTOCOL']),
                 's': response.status_code,
                 'b': str(len(response.content)),
                 'f': environ.get('HTTP_REFERER', ''),
                 'a': environ.get('HTTP_USER_AGENT', ''),
                 }
        for k, v in atoms.items():
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif not isinstance(v, str):
                v = str(v)
            # Fortunately, repr(str) escapes unprintable chars, \n, \t, etc
            # and backslash for us. All we have to do is strip the quotes.
            v = repr(v)[1:-1]
            # Escape double-quote.
            atoms[k] = v.replace('"', '\\"')
        
        try:
            self.access_log.log(logging.INFO, self.access_log_format % atoms)
        except:
            self.error(traceback=True)


if __name__ == '__main__':
    Server().run()

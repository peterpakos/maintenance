#!/usr/bin/env python

from __future__ import print_function
from sys import stderr, argv
from os import path, getuid
from time import sleep
from getopt import getopt, GetoptError
from re import split
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from threading import Thread


class Main(object):
    __version = '1.0'
    __name = path.basename(argv[0])
    __cwd = path.dirname(path.abspath(argv[0]))
    __ports = [8080]
    __servers = []

    def __init__(self):
        self.parse_options()

        for port in self.__ports:
            try:
                port = int(port)
            except ValueError:
                self.die('Port needs to be an integer number')

            if port <= 1024 and not self.is_root():
                self.die('Port %s requires root privileges' % port)

            if not path.isfile('index.html'):
                self.create_index_html()

            httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
            self.__servers.append(httpd)
            print('Serving Maintenance HTTP server on %s:%s' %
                  (httpd.socket.getsockname()[0], httpd.socket.getsockname()[1]))
            Thread(target=httpd.serve_forever).start()

        try:
            while True:
                sleep(.1)
        except KeyboardInterrupt:
            for httpd in self.__servers:
                httpd.shutdown()

    def parse_options(self):
        options = None

        try:
            options, args = getopt(argv[1:], 'hvp:c', [
                'help',
                'version',
                'port=',
                '--create-html'
            ])
        except GetoptError as err:
            self.die(err)

        for opt, arg in options:
            if opt in ('-v', '--version'):
                self.display_version()
                exit()
            if opt in ('-h', '--help'):
                self.display_usage()
                exit()
            if opt in ('-p', '--port'):
                self.__ports = sorted(split(' +|[.,;]', arg))
            if opt in ('-c', '--create-html'):
                self.create_index_html()
                self.die()

    def display_version(self):
        print('%s version %s' % (self.__name, self.__version))

    def display_usage(self):
        self.display_version()
        print('''Usage: %s [OPTIONS]
AVAILABLE OPTIONS:
-h, --help         Print this help summary page
-v, --version      Print version number
-p, --port         Port number[s] (default: 8080)
-c, --create-html  Create index.html page and exit''' % self.__name)

    @staticmethod
    def die(message=None, code=1):
        if message is not None:
            print(message, file=stderr)
        exit(code)

    @staticmethod
    def is_root():
        if getuid() == 0:
            return True
        else:
            return False

    @staticmethod
    def create_index_html():
        print('Creating index.html file: ', end='')
        html = '''<!doctype html>
<meta charset="UTF-8">
<title>Site Maintenance</title>
<style>
  body { text-align: center; padding: 20px; }
  @media (min-width: 768px){
    body{ padding-top: 150px; }
  }
  h1 { font-size: 50px; }
  body { font: 20px Helvetica, sans-serif; color: #333; }
  article { display: block; text-align: left; max-width: 650px; margin: 0 auto; }
  a { color: #dc8100; text-decoration: none; }
  a:hover { color: #333; text-decoration: none; }
</style>
<body>
<article>
    <h1>Maintenance in progress...</h1>
    <div>
        <p>Sorry for the inconvenience but we&rsquo;re performing some maintenance at the moment. If you need to you can always <a href="mailto:infra@wandisco.com?subject=Site Maintenance">email us</a> or <a href="http://helpdesk.wandisco.com" target="_blank">raise an IT ticket</a>, otherwise the site will be back online shortly!</p>
        <p>&mdash; Infrastructure & IT Team</p>
    </div>
</article>
</body>'''
        fh = open('index.html', 'w')
        fh.write(html)
        fh.close()
        print('DONE')

if __name__ == '__main__':
    app = Main()

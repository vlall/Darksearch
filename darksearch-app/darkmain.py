#!/usr/bin/python

import os
import json
import urllib2
import time
import sys
import requests
from darkspace import BackCheck
import logging
from logging.handlers import RotatingFileHandler
import threading
from time import gmtime, strftime
from flask import Flask, url_for, request, render_template
from flask import redirect, Markup, session, abort, send_from_directory
from flask_limiter import Limiter

app = Flask(__name__)
limiter = Limiter(
                    app, global_limits=[
                                        "2000 per day",
                                        "400 per hour",
                                        "60 per minute"
                        ]
        )


def deFace(alias):
    """
    Run query from darkspace.BackCheck.
    """
    search = BackCheck(alias)
    return search


@app.route("/", methods=['POST', 'GET'])
@limiter.limit("3/second")
def index():
    return render_template('index.html')


@app.route("/search/<int:page>", methods=['POST', 'GET'])
@limiter.limit("3/second")
def search(page=1):
    start_time = time.time()
    try:
        alias = request.form['search']
    except:
        try:
            alias = session['query']  # Check cookies.
        except:
            abort(400)
    alias = deFace(alias)
    engineList = alias.darkSites(page)
    query = str(alias.query)
    session['query'] = query
    results = str(alias.numDark)
    pageTotal = str(alias.maxPages)
    pageBar = alias.pageBar  # Do not turn to str.
    dur = ('%.3f') % (time.time() - start_time)
    make_logs(query, dur, results, page)
    return render_template(
                            'search.html',
                            dur=dur,
                            results=results,
                            query=query,
                            engineList=engineList,
                            pageTotal=pageTotal,
                            pageBar=pageBar
            )


@app.route("/<onion>", methods=['POST', 'GET'])
def link(onion):
    onion = onion.replace('.html', "")
    return send_from_directory('data', onion+'.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html', notice=e.description), 429


def make_logs(query, dur, results, page):
    """
    Log site search traffic in /logs.
    """
    ip = request.environ.get("REMOTE_ADDR")
    clock = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    log = '%s, %s, %s, %s, results:%s, page:%s' % (
                                                    clock,
                                                    ip,
                                                    query,
                                                    dur,
                                                    results,
                                                    page
                                                )
    app.logger.info(log)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)  # Creates 24-char cookie
    handler = RotatingFileHandler(
                                'logs/info.log',
                                maxBytes=10000,
                                backupCount=1
                )
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(
            host='0.0.0.0',
            port=80,
            debug=True,
            threaded=True
    )

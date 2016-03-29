#!/usr/bin/python

import os
import json
import urllib2
import time
import sys
import requests
import logging
import threading
from logging.handlers import RotatingFileHandler
from darkspace import BackCheck
from time import gmtime, strftime
from flask import Flask, url_for, request, render_template
from flask import redirect, Markup, session, abort, send_from_directory
from flask.ext.api import FlaskAPI, status, exceptions
from flask_limiter import Limiter
from flask import jsonify
from pympler import tracker


app = Flask(__name__)
limiter = Limiter(
                    app, global_limits=[
                                        "2000 per day",
                                        "400 per hour",
                                        "60 per minute"
                        ]
        )
app.secret_key = os.urandom(24)  # Creates 24-char cookie
handler = RotatingFileHandler(
                            'darksearch/logs/info.log',
                                maxBytes=100000,
                            backupCount=10
            )
handler.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)


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
    if page > pageTotal:
        abort(404)
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
    root_dir = os.path.dirname(os.getcwd())
    #  print root_dir
    return send_from_directory(os.path.join(root_dir, 'darksearch/darksearch/data'), onion+'.html')

"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html', notice=e.description), 429
"""

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


# API SECTION
@app.route("/api/<text>/<int:page>", methods=['GET'])
@limiter.limit("3/second")
def user_get(text, page=1):
    start_time = time.time()
    alias = text
    alias = deFace(alias)
    engineList = alias.darkSites(page)
    query = str(alias.query)
    results = str(alias.numDark)
    pageTotal = str(alias.maxPages)
    dur = ('%.3f') % (time.time() - start_time)
    make_logs(query, dur, results, page)
    if page > pageTotal:
        return '404 Error'
    return jsonify(
                    {
                        'query': '%s' % query,
                        'size': '%s' % results,
                        'total_pages': '%s' % pageTotal,
                        'duration': '%s' % dur
                    }
            )


if __name__ == '__main__':
    app.run(
            host='0.0.0.0',
            port=80,
            debug=True,
            threaded=True
    )

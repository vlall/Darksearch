#!/usr/bin/python

import json
import urllib2
import time
import sys
import requests
from flask import Flask, url_for, request, render_template, redirect, Markup
from darkspace import BackCheck
import logging
from logging.handlers import RotatingFileHandler
import threading
from time import gmtime, strftime

app = Flask(__name__)

def deFace(alias):
	"""
	Run query from darkspace.BackCheck.
	"""
	search = BackCheck(alias)
	return search

@app.route("/", methods=['POST', 'GET'])
def index():
	return render_template('index.html') 

@app.route("/search", methods=['POST', 'GET'])

def search():
	"""
	Grab clearnet information and compate it to .onion metadata. 
	"""
	# Present time it takes to run.
	start_time = time.time()
	alias = request.form['search']
	alias = deFace(alias)

	# Markup lets you embed python strings as HTML code.
	facebook = Markup(alias.searchResults('Facebook-','facebook', alias.facebook, 'Social Media'))
	twitter = Markup(alias.searchResults('Twitter-','twitter', alias.twitter, 'Social Media'))
	youtube = Markup(alias.searchResults('YouTube-','youtube', alias.youtube, 'Social Media'))
	linkedin = Markup(alias.searchResults('Linkedin-','linkedin', alias.linkedin, 'Social Media'))
	github = Markup(alias.searchResults('Github-','github', alias.github, 'Programming'))
	instagram = Markup(alias.searchResults('Instagram-','instagram', alias.instagram, 'Social Media'))
	gplus = Markup(alias.searchResults('Google Plus-', 'google', alias.gplus, 'Social Media'))
	tor = Markup(alias.searchResults('Tor-', 'tor', alias.torLinks, 'Dark Web'))
	dur = str(time.time() - start_time)
	results = str(alias.resultSize())
	query = alias.query
	make_logs(query, dur, results)
	return render_template('search.html', facebook=facebook, twitter=twitter, instagram=instagram, youtube=youtube, linkedin=linkedin, github=github, tor=tor, dur=dur, results=results, query=query, gplus=gplus)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 404

def make_logs(query, dur, results):
	"""
	Log site search traffic in /logs.
	"""
	ip = request.environ.get("REMOTE_ADDR")
	clock = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	log = '%s, %s, %s, %s, results:%s'%(clock, ip, query, dur, results)
	app.logger.info(log)


if __name__ == '__main__':
	handler = RotatingFileHandler('logs/info.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)


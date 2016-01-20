#!/usr/bin/python

import json
import urllib2
import time
import sys
import requests
from flask import Flask, url_for, request, render_template, redirect, Markup
from darkspace import BackCheck

# DarkSearch, a search engine running flask that looks at clearnet information and compates it to .onion metadata. 
app = Flask(__name__)

# This runs from the darkspace.BackCheck function, and is the search engine
def deFace(alias):
	search = BackCheck(alias)
	return search

# Home page search function 
@app.route("/", methods=['POST', 'GET'])
def index():
	return render_template('index.html') 

# Search method that provides us with results
@app.route("/search", methods=['POST', 'GET'])
def search():
	alias = request.form['search']
	alias = deFace(alias)

	# Markup lets you embed python strings as HTML code 
	facebook = Markup(alias.searchResults('Facebook', alias.facebook, 'Social Media'))
	twitter = Markup(alias.searchResults('Twitter', alias.twitter, 'Social Media'))
	youtube = Markup(alias.searchResults('Youtube', alias.youtube, 'Social Media'))
	linkedin = Markup(alias.searchResults('Linkedin', alias.linkedin, 'Social Media'))
	github = Markup(alias.searchResults('Github', alias.github, 'Programming'))
	tor = Markup(alias.searchResults('Tor', alias.torLinks, 'Dark Web'))
	return render_template('search.html', facebook = facebook, twitter = twitter, youtube=youtube, linkedin =linkedin, github = github, tor = tor)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 404

# Main Flask loop
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)



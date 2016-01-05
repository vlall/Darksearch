import json
import urllib2
import time
import sys
import requests
from flask import Flask, url_for, request, render_template, redirect
from darkspace import BackCheck
from flask import Markup

# DarkSearch, a search engine running flask that looks at .onion metadata, and compares it with clearnet information. 
app = Flask(__name__)

# This runs from the darkspace.BackCheck function, and is the search engine
def deFace(alias):
	x = BackCheck(alias)
	return x

# Home page search function 
@app.route("/", methods=['POST', 'GET'])
def index():
	return render_template('index.html') 

# Search method that provides us with results
@app.route("/search", methods=['POST', 'GET'])
def search():
	alias = request.form['search']
	alias = deFace(alias)

	#---OLD---
	#These orignially generated just the variables, not formtted into HTML lists
	#facebook = alias.facebook
	#twitter = alias.twitter
	#youtube = alias.youtube
	#linkedin = alias.linkedin
	#---END OLD--

	# Markup lets you embed python strings as HTML code 
	facebook = Markup(alias.searchResults('Facebook', alias.facebook, 'Social Media'))
	twitter = Markup(alias.searchResults('Twitter', alias.twitter, 'Social Media'))
	youtube = Markup(alias.searchResults('Youtube', alias.youtube, 'Social Media'))
	linkedin = Markup(alias.searchResults('Linkedin', alias.linkedin, 'Social Media'))
	github = Markup(alias.searchResults('Github', alias.github, 'Programming'))
	# TODO: Add Darkweb search functionality
	tor = Markup(alias.searchResults('Tor', alias.github, 'Dark Web'))

	return render_template('search.html', facebook = facebook, twitter = twitter, youtube=youtube, linkedin =linkedin, github = github, tor = tor)

# There error handlers are for exceptions.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 404

# Main Flask loop
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



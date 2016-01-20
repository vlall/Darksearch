#!/usr/bin/python

import json
import urllib2
import time
import sys
import requests
import re
from bs4 import BeautifulSoup
from lxml import html

'''
class BackCheck is responsible for taking a user query ex: "John Smith"
in darkmain.py and retrieving useful information from the clearnet,
relating it to scraped .onion sites etc. 
'''
class BackCheck(object):


	def __init__(self, query, dob=None):
		# If there's a birthdate in the query, 19??. Take it and search usernames
		regexDob = re.compile('19..')
		dob = [string for string in query.split() if re.match(regexDob, string)]
		# Lets only use one birthdate... Change this later
		if dob:
			dob = dob[0]
			query = query.replace(dob,"")
		print query
		'''
		# adding flags.
			self.sections= query.split(',')
			for i in self.sections:
				flagKey = self.sections.split('--')[1]
				flagValue = self.sections.split('--')[0]
			if flagKey == 'user':
		'''
		self.dob = dob
		self.query = query
		leads = self.nameChk()
		self.output = self.checkSites(leads)

	def nameChk(self):
		usernames = []
		fullnames = []
		fullnames.append(self.query)
		for i in fullnames:
			nameList=i.split()
			firstLetter = nameList[0][0]
			firstName = nameList[0]
			lastName = nameList[-1]
			lastLetter = nameList[-1][0]

			# If a middlename exists, lets add it to the mix
			mid = nameList[1:-1]
			if mid:
				middleName = ', '.join(mid)
				middleLetter = ', '.join(mid)
				usernames.append(lastName+middleName+firstName)
				usernames.append(lastName+middleLetter+firstName)

			# If Date of Birth is a parameter, lets add that as well
			if self.dob:
				dob = self.dob
				dobLast2 = self.dob[-2:]
				usernames.append(firstName+lastName+dob)
				usernames.append(firstLetter+lastName+dob)
				usernames.append(firstName+lastName+dobLast2)
				usernames.append(firstLetter+lastName+dobLast2)

			# General parameters that should exist in the original query
			if nameList>1:
				usernames.append(firstLetter+lastName)
				usernames.append(firstName+lastName)
				usernames.append(lastName+firstName)
			if nameList<=1:
				usernames.append(firstName)
					
		# Return the list of potential usernames from the above
		self.usernames = usernames
		usernames = set(usernames)
		return usernames

	# Check websites if profiles exist, beware of rate limiting, should use APIs for this
	def response200(self,socialList, website, username, socialName='site'):
		#connect_timeout = 1
		#read_timeout = 5.0
		website = website + str(username)
		#Old Request method
		httpResp = requests.get(website, stream=True)#, timeout=(connect_timeout, read_timeout))
		#httpResp = requests.head(website,stream=True, allow_redirects=True)
		if httpResp.status_code == 200:
			socialList.append(website)
			print 'Potential %s Found...' % socialName 
		else:
			print 'Search Fail...'

	def dark200(self, socialList, username):
		pass

	# Scrape all of the profile images on a webpage. 
	def imageResuts(self, links):
		pass

	def checkSites(self, usernames):
		output = []
		self.twitter = []
		self.facebook = []
		self.youtube = []
		self.linkedin = []
		self.github = []
		self.torLinks = []
		self.torResults = []
		for i in usernames:
			output.append(i)
		# Check potential social media using the response200() method
			self.response200(self.twitter, 'http://twitter.com/', i, 'Twitter')
			self.response200(self.facebook, 'http://facebook.com/', i, 'Facebook')
			self.response200(self.youtube, 'https://youtube.com/user/', i, 'YouTube')
			self.response200(self.linkedin, 'http://linkedin.com/in/', i, 'LinkedIn')
			self.response200(self.github, 'http://github.com/', i, 'GitHub')
			self.onion_check(self.query, i)
		return output

	def onion_check(self, query, alias):
		page = requests.get('https://ahmia.fi/search/?q=%s' % query)
		tree = html.fromstring(page.content)
		results = tree.xpath('.//cite/text()')
		print results
		for i in results:
			self.torLinks.append('http://%s' % i)
	
	# This function gets called in darkmain.py. It is meant to display each item as an HTML <li> for search.html
	def searchResults(self, socialName, link, category='website'):
		lowerName = socialName.lower()
		hrefs = ""
		for i in link:
			nLink = "<p class=\"description\"> <a href=\"%s\">%s</a> </p>" % (str(i), str(i))
			hrefs = str(nLink + hrefs)
		if not link:
			hrefs = "<p class=\"description\">Potential items not found or are hidden</p><br>"
		self.results = "<li> <img src=\"../static/listjs/images/icons/%s.png\" class=\"thumb\" /><h4><span class=\"name\">%s</span> <span class=\"category\">%s</span></h4><p class=\"description\"> %s</p> </li>" % (lowerName, socialName, category, hrefs)
		return self.results

	# Make function that prints the Darkweb results organized by query. 
	def darkSites(self, torResults):
		pass

if __name__ == '__main__':
	example = BackCheck('John Smith')
	print example.output

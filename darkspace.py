import json
import urllib2
import time
import sys
import requests
#from validate_email import validate_email
'''
class BackCheck is responsible for taking a user query ex: "John Smith"
in darkmain.py and retrieving useful information from the clearnet,
relating it to scraped .onion sites etc. 
'''
class BackCheck(object):
	def __init__(self, query, dob=None):
		# Deal with flags in a query
		self.query = query

		'''
			self.sections= query.split(',')
			for i in self.sections:
				flagKey = self.sections.split('--')[1]
				flagValue = self.sections.split('--')[0]
			if flagKey == 'user':
		'''

		self.dob = dob
		y = self.nameChk()
		self.output = self.checkSites(y)

	'''
	This function makes potential usernames from the given parameters
	Usually, the parameters are a string of potential names, 
	where we test each name out for information below
	'''
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
				dobLast2 = self.dob[-2:]
				usernames.append(firstName+lastName+dob)
				usernames.append(firstLetter+lastName+dob)
				usernames.append(firstName+lastName+dobLast2)
				usernames.append(firstLetter+lastName+dobLast2)

			# General parameters that should exist in the original query
			usernames.append(firstLetter+lastName)
			usernames.append(firstName+lastName)
			usernames.append(lastName+firstName)

		# Return the list of potential usernames from the above
		self.usernames = usernames
		return usernames

	# Check websites if profiles exist, beware of rate limiting, should use APIs for this
	def response200(self,socialList, website, username, socialName='site'):
		#connect_timeout = 1
		#read_timeout = 5.0

		website = website + str(username)
		#Old Request method
		r = requests.get(website, stream=True)#, timeout=(connect_timeout, read_timeout))
		#r = requests.head(website, allow_redirects=True)
		if r.status_code == 200:
			socialList.append(website)
			print 'Potential %s Found...' % socialName 

	# This function gets called in darkmain.py. It is meant to display each item as an HTML <li> for search.html
	def searchResults(self, socialName, link, category='website'):
		lowerName = socialName.lower()
		hrefs = ""
		for i in link:
			nLink = "<p class=\"description\"> <a href=\"%s\">%s</a> </p>" % (str(i), str(i))
			hrefs = str(nLink + hrefs)
		if not link:
			hrefs = "<p class=\"description\">Potential items not found or are hidden</p><br>"
		self.results = "<li> <img src=\"../static/listjs/images/icons/%s.png\" class=\"thumb\" /><h4><span class=\"name\">%s</span> <span class=\"category\">%s</span></h4><p class=\"description\"> %s</p></li>" % (lowerName, socialName, category, hrefs)
		return self.results

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
		for i in usernames:
			output.append(i)

		# Check potential social media using the response200() method
			self.response200(self.twitter, 'http://www.twitter.com/', i, 'Twitter')
			self.response200(self.facebook, 'http://www.facebook.com/', i, 'Facebook')
			self.response200(self.youtube, 'https://www.youtube.com/user/', i, 'YouTube')
			self.response200(self.linkedin, 'http://www.linkedin.com/in/', i, 'LinkedIn')
			self.response200(self.github, 'http://www.github.com/', i, 'GitHub')

		return output

	# TODO: Submit API tokens from main conf file
	def social_media(self):
		pass
	
if __name__ == '__main__':
	x = BackCheck('John Smith')
	print x.output

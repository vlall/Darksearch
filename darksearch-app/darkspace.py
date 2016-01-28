#!/usr/bin/python

from engine import SearchEngine
import json
import urllib2
import time
import requests
import re
from bs4 import BeautifulSoup
from lxml import html
from flask import Flask, url_for, request, render_template, redirect, Markup
import sys  
import math


reload(sys)  
sys.setdefaultencoding('utf8')


class BackCheck(object):
    """
    Take user query ex: "John Smith" in darkmain.py and retrieve useful
    information from the clearnet,relating it to scraped .onion sites etc.
    """

    def __init__(self, query, dob=None):
        # Removes all non-alphanumeric, non-white space characters
        query = re.sub(r'[^a-zA-Z\d\s:]', '', query)
        # If there's a birthdate in the query, 19??.
        # Take it and search usernames
        regexDob = re.compile('19..')
        dob = [string for string in query.split() if re.match(regexDob, string)]
        # Lets only use one birthdate... Change this later
        if dob:
            dob = dob[0]
            query = query.replace(dob, "")
        print query

        self.dob = dob
        self.query = query
      #  leads = self.nameChk()
      #  self.output = self.checkSites(leads)

    def nameChk(self):
        usernames = []
        fullnames = []
        fullnames.append(self.query)

        # If there's only one name in the list...
        if len(self.query.split(' ')) == 1:
            return fullnames
        for i in fullnames:
            nameList = i.split()
            firstLetter = nameList[0][0]
            firstName = nameList[0]
            lastName = nameList[-1]
            lastLetter = nameList[-1][0]
            #  If a middlename exists, lets add it to the mix
            mid = nameList[1:-1]
            if mid:
                middleName = ', '.join(mid)
                middleLetter = ', '.join(mid)
                usernames.append(lastName+middleName+firstName)
                usernames.append(lastName+middleLetter+firstName)
            #  If Date of Birth is a parameter, lets add that as well
            if self.dob:
                dob = self.dob
                dobLast2 = self.dob[-2:]
                usernames.append(firstName+lastName+dob)
                usernames.append(firstLetter+lastName+dob)
                usernames.append(firstName+lastName+dobLast2)
                usernames.append(firstLetter+lastName+dobLast2)
            #  General parameters that should exist in the original query
            if nameList > 1:
                usernames.append(firstLetter+lastName)
                usernames.append(firstName+lastName)
                usernames.append(lastName+firstName)
            if nameList <= 1:
                usernames.append(firstName)
        #  Return the list of potential usernames from the above
        self.usernames = usernames
        usernames = set(usernames)
        return usernames

    def response200(self, socialList, website, username, socialName='site'):
        """
        Check if profiles exist, beware of rate limiting.
        """
        website = website + str(username)
        httpResp = requests.get(
                    website, stream=True
                ) 
        #  Old Request method
        #  httpResp = requests.head(website,stream=True, allow_redirects=True)
        if httpResp.status_code == 200:
            socialList.append(website)
            print 'Potential %s Found...' % socialName
        else:
            print 'Search Fail...'

    def dark200(self, socialList, username):
        pass

    def imageResuts(self, links):
        """Scrape all of the profile images on a webpage."""
        pass

    def checkSites(self, usernames):
        """
        Save site status to Array.
        """
        output = []
        self.twitter = []
        self.facebook = []
        self.youtube = []
        self.linkedin = []
        self.github = []
        self.instagram = []
        self.gplus = []
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
            self.response200(self.instagram, 'http://instagram.com/', i, 'Instagram')
            self.response200(self.gplus, 'http://plus.google.com/+', i, 'Google')
        # Search Origininal Query on Dark Web.
        self.onion_check(self.query, i)
        return output

    def onion_check(self, query, alias):
        """
        Temporary: Checks ahmia for onions.
        """
        page = requests.get('https://ahmia.fi/search/?q=%s' % query)
        tree = html.fromstring(page.content)
        results = tree.xpath('.//cite/text()')
        print results
        for i in results:
            self.torLinks.append('http://%s' % i)

    def searchResults(self, socialName, image, link, category='website'):
        """
        Display each item as an HTML <li> for search.html
        Gets called in darkmain.py.
        """
        lowerName = socialName.lower()
        hrefs = ""
        for i in link:
            nLink = "<p class=\"description\"> <a href=\"%s\">%s</a> </p>" % (str(i), str(i))
            hrefs = str(nLink + hrefs)
        if not link:
            hrefs = "<p class=\"description\">Potential items not found or are hidden</p>"
        self.results = "<li> <img src=\"../static/listjs/images/icons/%s.png\" class=\"thumb\" /><h4><span class=\"name\">%s</span> <span class=\"category\">%s</span></h4><p class=\"description\"> %s </p> </li>" % (image, socialName, category, hrefs)
        return self.results

    def darkResults(self, socialName, image, description, href, category='website'):
        description=str(description)
        lowerName = socialName.lower()
        hrefs = ""
        if description:
            nLink = "<p class=\"description\">%s...</p>" % (description)
        if not description:
            hrefs = "<p class=\"description\">Potential items not found or are hidden</p>"
        self.results = "<li> <img src=\"../static/listjs/images/icons/%s.png\" class=\"thumb\" /><h4><span class=\"name\"><a href=../data/%s><br> %s </font></a> </span> <span class=\"category\"><br>updated: %s</span></h4><p class=\"description\"><br>%s </p> </li>" % (image, href, socialName, category, description)
        return self.results
    
    def make_pageBar(self, current, end):
        start = 1
        results = ""
        back = ""
        next = ""
        if end >= 5:
            end = current + 2
        if current >= 3:
            start = current - 2
        if end > self.maxPages:
             end = self.maxPages
        for page in range(start, end + 1):
            if page == current: 
                line = "<li ><a href=\"../search/%s\" method=\"post\"><font color=\"red\"><b>%s</b></font> </a></li>" % (page, page)
            else:    
                line = "<li ><a href=\"../search/%s\" method=\"post\">%s </a></li>" % (page, page)
            results = results + line
        if (current - 1) > 0:
            back = "<li ><a href=\"../search/%s\" method=\"post\"> Prev </a></li>" % (current - 1)
        if (current + 1) <= end:
            next = "<li ><a href=\"../search/%s\" method=\"post\"> Next </a></li>" % (current + 1)
        return (back + results + next)

    # <li ><a href="{{ url_for('search',page=1) }}" method="post"> Last </a></li>
    #  <li ><a href="{{ url_for('search',page=1) }}" method="post"> Next </a></li>

    def darkSites(self, currentPage, limitResults=10):
        test = SearchEngine()
        test.search(self.query)
        darkList=test.names.tolist()
        results = test.contentList
        self.maxPages = int(math.ceil(len(results) / float(limitResults)))
        self.numDark = len(results)
        display = test.briefList
        descTotal = ''
        #  Display 20 results per page
        displayStart = (currentPage * limitResults) - limitResults
        displayEnd = (currentPage * limitResults) 
        for val in display[int(displayStart):int(displayEnd)]:
            i = display.index(val)
            description = Markup(
            self.darkResults(
                darkList[i],
                'tor',
                unicode(val, errors='ignore'),
                darkList[i],
                test.dates.tolist()[i].split()[0]
                )
            )
            descTotal = descTotal + description
        self.pageBar = Markup(self.make_pageBar(currentPage, self.maxPages))
        return Markup(descTotal)


    def resultSize(self):
        """
        Generate Number of results
        """
        results = (
                len(self.twitter) +
                len(self.facebook) +
                len(self.youtube) +
                len(self.linkedin) +
                len(self.github) +
                len(self.torLinks)
        )
        return results


if __name__ == '__main__':
    example = BackCheck('John Smith')
    print example.output

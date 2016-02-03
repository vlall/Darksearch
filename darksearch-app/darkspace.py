#!/usr/bin/python

import json
import urllib2
import time
import requests
import re
import sys
import math
import gc
from tools import DarkElastic
from flask import Flask, url_for, request, render_template, redirect, Markup

reload(sys)
sys.setdefaultencoding('utf8')


class BackCheck(object):
    """
    Search .onions for keywords
    """

    def __init__(self, query, dob=None):
        #  Removes all non-alphanumeric, non-white space characters
        query = re.sub(r'[^a-zA-Z\d\s:]', '', query)
        self.query = query

    def dark200(self, socialList, username):
        pass

    def imageResuts(self, links):
        """Scrape all of the profile images on a webpage."""
        pass

    def darkResults(self, socialName, image, description, href, category='website'):
        description = str(description)
        hrefs = ""
        href = href.replace('.html', "")
        if description:
            nLink = "<p class=\"description\">%s...</p>" % (description)
        if not description:
            hrefs = "<p class=\"description\">Potential items not found or are hidden</p>"
        self.results = (
                        "<li> <img src=\"../static/listjs/images/icons/%s.png\""
                        " class=\"thumb\" /><h4><span class=\"name\"><a href=../%s>"
                        " <p style=\"font-size:14px; color:#517aa3; text-decoration: "
                        "underline;\">%s</p></a> </span> <span class=\"category\">"
                        "<p style=\"font-size:11px\">updated: %s</p></span>"
                        "</h4><p class=\"description\">%s </p> </li>" 
                        % (image, href, socialName, category, description)
        )
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
        else:
            end = current + (5 - current)
        if end > self.maxPages:
            end = self.maxPages
        for page in range(start, end + 1):
            if page == current:
                line = (
                        "<li ><a href=\"../search/%s\" method=\"post\">"
                        "<font color=\"red\"><b>%s</b></font> </a></li>" 
                        % (page, page)
                )
            else:
                line = "<li ><a href=\"../search/%s\" method=\"post\">%s </a></li>" % (page, page)
            results = results + line
        if (current - 1) > 0:
            back = "<li ><a href=\"../search/%s\" method=\"post\"> Prev </a></li>" % (current - 1)
        if (current + 1) <= end:
            next = "<li ><a href=\"../search/%s\" method=\"post\"> Next </a></li>" % (current + 1)
        return (back + results + next)

    def darkSites(self, currentPage, limitResults=10):
        #  Start ElasticSearch
        gc.collect()
        elastic = DarkElastic()
        elastic.search_index('dark', self.query)
        self.numDark = elastic.size
        self.maxPages = math.ceil((self.numDark) / float(limitResults))
        self.maxPages = int(self.maxPages)
        #  Displays 10 results per page
        displayStart = int((currentPage * limitResults) - limitResults)
        displayEnd = int((currentPage * limitResults))
        elastic.search_index('dark', self.query, displayStart, limitResults)
        darkList = elastic.namesList
        dates = elastic.datesList
        display = elastic.briefList
        title = elastic.titleList
        descTotal = ''
        self.pageBar = Markup(self.make_pageBar(currentPage, self.maxPages))
        for val in display:
            cat = elastic.check_cat(val)
            i = display.index(val)
            description = Markup(
                                    self.darkResults(
                                                        title[i],
                                                        cat,
                                                        val,
                                                        darkList[i],
                                                        elastic.datesList[i]
                                                        )
                        )
            descTotal = descTotal + description
        return Markup(descTotal)


if __name__ == '__main__':
    example = BackCheck('John Smith')
    print example.output

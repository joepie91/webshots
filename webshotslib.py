#!/usr/bin/python

import urllib, re

def get_category_listings(url):
	contents = urllib.urlopen(url).read()
	matches = re.findall('<a href="(http:\/\/www\.webshots\.com\/members\/[^/]+\/[^/]+\.html)">top members</a>', contents)
	return matches

def get_user_listings(url):
	contents = urllib.urlopen(url).read()
	matches = re.findall('<a href="(http:\/\/www\.webshots\.com\/members\/[^/]+\/[^/]+\.html)">[0-9]+-[0-9]+</a>', contents)
	
	if len(matches) > 0:
		matches.pop(0)
		
	return matches

def get_users(url, allow_quotes):
	contents = urllib.urlopen(url).read()
	
	if allow_quotes == True:
		matches = re.findall('http:\/\/community\.webshots\.com\/user\/([^/]+)', contents)
	else:
		matches = re.findall('http:\/\/community\.webshots\.com\/user\/([^/\'"]+)', contents)
	
	count = contents.count("http://community.webshots.com/user/")
	
	return [value for value in matches if value != "my"], count

def search_query(query):
	query = urllib.quote(query.ljust(3, "%") + "%")
	return get_users("http://www.webshots.com/explore/member?action=userSearch&username=%s" % query, True)

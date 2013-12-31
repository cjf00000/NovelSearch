# -*- coding: utf-8
import urllib, urllib2
from bs4 import BeautifulSoup

def post(url, data):
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
	header = { 'User-Agent' : user_agent }

	request = urllib2.Request(url, urllib.urlencode(data), header)
	return urllib2.urlopen(request).read()

def fetch(query):
	results = []

	fetchBxwc(query, results)

	# TODO add other sites here
	# fetchOther1(query, results)
	# fetchOther2(query, results)
	# fetchOther3(query, results)
	# ...

	return results

def fetchBxwc(query, results):
	try:
		searchUrl = 'http://www.bxwx.cc/modules/article/search.php'	# search on the novel website
		searchData = { 'searchkey' : query.encode('gbk'), 'action' : 'login', 'button' : u'搜 索'.encode('gbk') }
										# html form to post, *careful with encoding!!*
		novelHtml = post(searchUrl, searchData).decode('gbk')		# search, get the novel html, *careful with encoding!!*

		novelSoup = BeautifulSoup(novelHtml)				# parse html
		novelMain = novelSoup.find(id='main')				# navigate down the html....
		novelButton = novelMain.find("li", "button2 white")
		for link in novelButton.find_all('a', "btnlink"):
			if (link.get_text() == u'TXT全集'):			# search for the tag......
				results.append(link.get('href'))

	except Exception as e:							# ignore all exceptions
		pass

def fetchOther(query, results):
	# TODO implement this several sites
	pass

if __name__ == '__main__':
	print fetch(u'武动乾坤')


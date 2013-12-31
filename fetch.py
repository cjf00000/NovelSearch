# -*- coding: utf-8
import urllib, urllib2
from bs4 import BeautifulSoup

def post(url, data):
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
	header = { 'User-Agent' : user_agent }

	request = urllib2.Request(url, urllib.urlencode(data), header)
	return urllib2.urlopen(request).read()

def get(url):
	return urllib2.urlopen(url).read()

def fetch(query):
	results = []

	fetchBxwc(query, results)
	print results
	fetchWxxs(query, results)
	print results

	# TODO add other sites here

	return results

def fetchBxwc(query, results):
	try:
		searchUrl = 'http://www.bxwx.cc/modules/article/search.php'	# search on the novel website
		searchData = { 'searchkey' : query.encode('gbk'), 'action' : 'login', 'button' : u'搜 索'.encode('gbk') }
										# html form to post, *careful with encoding!!*
		novelHtml = post(searchUrl, searchData).decode('gbk')		# search, get the novel html, *careful with encoding!!*
                #print novelHtml
		novelSoup = BeautifulSoup(novelHtml)				# parse html
		novelMain = novelSoup.find(id='main')                           # navigate down the html....
        	if (novelMain == None):
                        novelContents = novelSoup.find(id = 'content2')
                        novelOdd = novelContents.find_all(attrs={'class':'odd'})
                    
                        #print novelContents.find_all('a')
                        for link in novelOdd:
                                novelA = link.a
                                if(novelA == None):
                                        continue
                                newdata = {}
                                newhtml = post(novelA.get('href'),newdata).decode('gbk')
                                print novelA.get('href')
                                newsoup =  BeautifulSoup(newhtml)
                                print 'get newsoup'
                                newmain = newsoup.find(id = 'main')
                                outputfile = open('results.txt','w')
                                outputfile.write(str(newmain))
                                
                                name = str(newmain.find('h1'))
                                name = name[4:(len(name)-5)]
                                outputfile.write(name)
                                outputfile.close()
                                print 'get newmain'                               
                                novelButton = newmain.find("li", "button2 white")
                                for link2 in novelButton.find_all('a', "btnlink"):
                                        if (link2.get_text() == u'TXT全集'):			# search for the tag......
                                                results.append( (name.decode('utf-8', 'ignore'), link2.get('href')) )
                else:
                        novelButton = novelMain.find("li", "button2 white")
                        for link in novelButton.find_all('a', "btnlink"):
                                if (link.get_text() == u'TXT全集'):			# search for the tag......
                                        results.append( (query, link.get('href')) )

	except Exception as e:							# ignore all exceptions
		pass

def fetchWxxs(query, results):
	try:
		searchUrl = 'http://www.55x.cn/plus/search.php?type=title&'	# search on the novel website
		searchData = { 'q' : query.encode('gbk'), 'action' : 'login', 'button' : u'搜 索'.encode('gbk') }
										# html form to post, *careful with encoding!!*
		novelHtml = post(searchUrl, searchData).decode('gbk')		# search, get the novel html, *careful with encoding!!*

                outputfile = open('novelHtml.txt','w')		
		novelSoup = BeautifulSoup(novelHtml)
                outputfile.write(str(novelSoup))
                outputfile.close()
		novelList = novelSoup.find_all('a')
                for link in novelList:
                        novelHref = link.get('href')
                        tmp = novelHref.split('/')
                        if (len(tmp) < 4):
                                continue
                        if (not(tmp[3][0:3] == 'txt')):
                                continue
                        newdata = {}
                        newhref = 'http://www.55x.cn'+str(novelHref)
                        newhtml = get(newhref).decode('gbk')
                        #print newhtml
                        newsoup = BeautifulSoup(newhtml)
                        name = str(newsoup.find('h1'))
                        name = name[4:(len(name)-5)]
                        #print name.decode('utf-8','ignore')
                        #results.append(name.decode('utf-8','ignore'))
                        newdownload = newsoup.find(attrs={'class':'xiaye'})
                        #print newdownload
                        link = newdownload.a.get('href')
                        newhref = 'http://www.55x.cn'+str(link)
                        newhtml = get(newhref).decode('gbk')
                        newsoup = BeautifulSoup(newhtml)
                        download = newsoup.find(attrs={'class':'shuji'}).a                        
                        results.append((name.decode('utf-8','ignore'),'http://www.55x.cn'+str(download.get('href'))))
                        
	except Exception as e:							# ignore all exceptions
		pass

def fetchOther(query, results):
	# TODO implement this several sites
	pass

if __name__ == '__main__':
	results = []
	fetchWxxs(u'武动', results)
	print results

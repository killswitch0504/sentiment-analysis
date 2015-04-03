import sqlite3
import time
import urllib2
from urllib2 import urlopen
import re
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

def getData():
	try:
		i = 0
		page = 'http://feeds.feedburner.com/Mobilecrunch'
		sourceCode = opener.open(page).read()
		try:
			links = re.findall(r'<link.*>(.*/?ncid=rss)</link>',sourceCode)
			for link in links:
				print link
				itemSource = urllib2.urlopen(link).read()
				print 'VISITING::',link
				contents = re.findall(r'<p>(.*)</p>',itemSource)
				i = 0
				for content in contents:
					i += 1
					if re.findall(r'<img .*>',content):
						pass
					else:
						print i,content
				time.sleep(100)
		except Exception,e:
			print 'hey'+str(e)


	except Exception, e:
		print 'Exception in getData'
		print str(e)

getData()
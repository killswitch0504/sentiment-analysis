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
conn.text_factory = str
c = conn.cursor()


def main():
	try:
		query = "SELECT * FROM WordValue"
		startWord = []
		startWordVal = []
		for r1 in c.execute(query):
			startWord.append(r1[0])
			startWordVal.append(r1[1])
		i = 0
		while i < len(startWordVal):
			start = startWord[i]
			startVal = startWordVal[i]
			i += 1
			print start,startVal
			q = "SELECT * FROM syn WHERE word=?"
			c.execute(q,[(start)])
			data1 = c.fetchone()
			
			if data1 is None:
				page = 'http://www.thesaurus.com/browse/'+start+'?s=t'
				sourceCode = opener.open(page).read()
				sourceCodeSplit = sourceCode.split('<h2>Antonyms <span>for '+start+'</span></h2>')[0]
				words = re.findall(r'<span class="text">(\w*)</span>',sourceCodeSplit)
				for word in words:
					q1 = "SELECT * FROM WordValue WHERE word=?"
					c.execute(q1,[(word)])
					data =c.fetchone()
					if word is 'bad' and startVal is 1.0:
						pass
					elif data is None:
						c.execute("INSERT INTO WordValue values (?,?)",(word,startVal))
						conn.commit()
					else:
						print 'Already present!'
			else:
				pass
			c.execute("INSERT INTO syn values (?)",(start,))
			conn.commit()			
			print 'Completed:',start

	except Exception, e:
		print str(e)

main()
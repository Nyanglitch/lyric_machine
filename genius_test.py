import os
import sys
from sys import argv
import urllib.error
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

def genius_func(singer, song):
	singer = re.sub("[^a-z0-9A-Z ]", '', sys.argv[1]).replace(" ", "-").lower()
	song = re.sub("[^a-z0-9A-Z ]", '', sys.argv[2]).replace(" ", "-").lower()
	url="https://genius.com/" + singer + "-" + song + "-lyrics"
	singer = singer.title()
	song = '"' + song.title() + '"'


	try:
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		web_byte = urlopen(req).read()
		webpage = web_byte.decode('utf-8')

	except urllib.error.HTTPError as e:
		print('HTTPError: {}'.format(e.code))
		exit()
	except urllib.error.URLError as e:
		print('URLError: {}'.format(e.reason))
		exit()

	# beautifulsoup stuff
	#####################
	soup = BeautifulSoup(webpage, 'html.parser')

	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	#####################

	# head, sep, tail = text.partition(" Lyrics"[2])
	head2, sep2, tail2 = text.partition("More on Genius") # only head2 is useful

	def trunc_at(s, d):
	    "Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."
	    text = s.split(d, 4)
	    return text

	rawoutput = trunc_at(head2, ' Lyrics')
	output = singer + '\n' + song + rawoutput[3]

	return output

	# print(output)
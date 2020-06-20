import os
import sys
from sys import argv
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import os.path
from os import path

if len(sys.argv) < 2:
	print('No arguments passed. Try "help" argument.')
	exit()

if len(sys.argv) == 2 and sys.argv[1] == 'help':
	print('..........HELP..........\nPass singer and song name. You may use quotes (if name contains spaces), apostrophes, and any case.\nPerfect example if in doubt: acdc highwaytohell\nThe program will make a separate folder in your current directory for outputs.\nYou may use QuickSave feature -- pass "n" or "y" as a third argument.')
	exit()

switches = ['n', 'y']

if len(sys.argv) == 3:
	singer = sys.argv[1]
	song = sys.argv[2]

if len(sys.argv) > 3:
	singer = sys.argv[1]
	song = sys.argv[2]
	if sys.argv[3].lower() not in switches:
		print('Too many arguments. Try "help" once.')
		exit()
	else: 
		if len(sys.argv) > 4:
			print('Too many arguments. Try "help" once.')
			exit()
		else:
			quickswitch = sys.argv[3]

# make a dir // check an existing dir

if path.exists('lyric_machine') == False:
	os.mkdir("lyric_machine")

# input formatting

song_filename = song.replace('"', '')
singer_clean = singer.replace(' ', '').replace("'", "").replace("/", "").replace('"', '').lower()
song_clean = song_filename.replace(' ', '').replace("'", "").replace("/", "").lower()

# connections

url = 'https://www.azlyrics.com/lyrics/' + singer_clean + '/' + song_clean + '.html'

try:
    conn = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    print('HTTPError: {}'.format(e.code))
    print('Page does not exist. Try different input or different song :(')
    exit()
except urllib.error.URLError as e:
    print('URLError: {}'.format(e.reason))
    print('Page does not exist. Try different input or different song :(')
    exit()
else:
    html = urllib.request.urlopen(url).read()

# beautifulsoup stuff
#####################
soup = BeautifulSoup(html, 'html.parser')

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

# adding everything to the text file

out_file = open('messy_output.txt', 'w', encoding='utf8')
out_file.write(text)
out_file.close()

# cleaning up the output

out_file = open('messy_output.txt', 'r', encoding='utf8')
clear_out_file = open('lyric_machine/' + singer + ' -- ' + song_filename + '.txt', 'w', encoding='utf8')

whole_content = ''

cont = out_file.readlines() 
for i in range(0, len(cont)):
	whole_content = whole_content + cont[i]

# cleanup

head2, sep2, tail2 = whole_content.partition('" lyrics\n')
head, sep, tail = tail2.partition('\nSubmit Corrections')

# unwanted word removal
head3, sep3, tail3 = head.partition(' Lyrics')

# concatenation to get clear output
head = head3 + tail3

# outputs

clear_out_file.write(head)
print(head)

clear_out_file.close()
out_file.close()
os.remove('messy_output.txt')

# save or not?

def save_submit():
	save_or_not = input("Keep lyrics as a text file? (y/n): ").lower()
	if save_or_not == 'n':
		os.remove('lyric_machine/' + singer + ' -- ' + song_filename + '.txt')
	elif save_or_not == 'y':
		exit()
	elif save_or_not == 'u so cool!':
		print('Aww! Thank you!')
		save_submit()
	else:
		print("Letter not supported.")
		save_submit()

def quick_save():
	if quickswitch.lower() == 'n':
		os.remove('lyric_machine/' + singer + ' -- ' + song_filename + '.txt')
	elif quickswitch.lower() == 'y':
		exit()
	else:
		print("Quicksave crashed, letter not supported.")
		save_submit()

if len(sys.argv) < 4:
	save_submit()
else:
	quick_save()



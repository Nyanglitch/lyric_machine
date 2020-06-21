import os
import sys
from sys import argv
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import os.path
from os import path
import re

error_arg1 = 'No arguments passed. Try "help" argument.'
error_arg2 = 'Too many arguments. Try "help" once.'
error_arg3 = 'Not enough arguments. Try "help" once.'

# exit error 0 // all OK
# exit error 1 // argument error
# exit error 2 // connection error

switches = ['n', 'y', 'clear']
quickswitch = 'u'

if len(sys.argv) > 4:
	print(error_arg2)
	exit(1)
else:
	if len(sys.argv) > 3:
		if sys.argv[3].lower() in switches:
			singer = sys.argv[1]
			song = sys.argv[2]
			quickswitch = sys.argv[3].lower()
		else:
			print(error_arg2)
			exit(1)
	else:
		if len(sys.argv) > 2:
			singer = sys.argv[1]
			song = sys.argv[2]
		else:
			if len(sys.argv) > 1:
				if sys.argv[1] == 'help':
					print('\nWELCOME TO LYRIC MACHINE\n\n######## HELP ########\nPass singer and song name. You may use quotes (if name contains spaces), apostrophes, and any case.\nPerfect example if in doubt: acdc highwaytohell\nThe program will make a separate folder in your current directory for outputs.\n\n###### SWITCHES ######\nUse them as a third argument:\nN for no-save, console output;\nY for save, console output;\nCLEAR for save, no console output.')
					exit(0)
				else:
					print(error_arg3)
					exit(1)
			else:
				print(error_arg1)
				exit(1)

# make a dir // check an existing dir

if path.exists('lyric_machine') == False:
	os.mkdir("lyric_machine")

# input formatting

song_filename = song.replace('"', '')
singer_filename = singer.replace('"', '')
song_clean = re.sub("[^a-z0-9]", '', song_filename).replace(" ", '').lower()
singer_clean = re.sub("[^a-z0-9]", '', singer_filename).replace(" ", '').lower()

# the path concatenation

the_lyric_path = 'lyric_machine/' + singer_filename + ' -- ' + song_filename + '.txt'

# lyrics were saved previously? type it out and exit

if path.exists(the_lyric_path) == True:
	with open(the_lyric_path, 'r') as f:
		data = f.read()
		print(data)
		exit(0)

# sync

def sync_function():
	for i in range():
		pass # sync algorithm here

def sync_check(sync_switch):
	if sync_switch == 'sync':
		sync_function()


sync_check(quickswitch)

# connections

url = 'https://www.azlyrics.com/lyrics/' + singer_clean + '/' + song_clean + '.html'

try:
    conn = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    print('HTTPError: {}'.format(e.code))
    print('Page does not exist. Try different input or different song :(')
    exit(2)
except urllib.error.URLError as e:
    print('URLError: {}'.format(e.reason))
    print('Page does not exist. Try different input or different song :(')
    exit(2)
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

out_file = open('messy_output.txt', 'r', encoding='utf8')
clear_out_file = open(the_lyric_path, 'w', encoding='utf8')

whole_content = out_file.read()

# cleanup

head2, sep2, tail2 = whole_content.partition('" lyrics\n')
head, sep, tail = tail2.partition('\nSubmit Corrections')

# unwanted word removal
head3, sep3, tail3 = head.partition(' Lyrics')

# concatenation to get clear output
head = head3 + tail3

# outputs

clear_out_file.write(head)

clear_out_file.close()
out_file.close()
os.remove('messy_output.txt')

# save or not?

def output_print(output_switch):
	if output_switch != 'clear':
		print(head)

def delete_output():
	os.remove(the_lyric_path)

def switch_check(arg):
	if arg == 'n':
		delete_output()
		exit(0)
	elif arg in ['y', 'clear']:
		exit(0)
	else:
		arg = input("Keep lyrics as a text file? (y/n): ").lower()
		switch_check(arg)

output_print(quickswitch)
switch_check(quickswitch)

exit(0)
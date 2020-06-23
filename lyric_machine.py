import os
import sys
from sys import argv
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import os.path
from os import path
import re
import genius_test

error_arg1 = 'No arguments passed. Try "help" argument.'
error_arg2 = 'Too many arguments. Try "help" once.'
error_arg3 = 'Not enough arguments. Try "help" once.'
error_arg4 = 'Page does not exist. Try different input or different song :('

# exit error 0 // all OK
# exit error 1 // argument error
# exit error 2 // connection error

switches = ('n', 'y', 'clear')
quickswitch = 'u'
the_packet = 'u'

# make a dir // check an existing dir

if path.exists('lyric_machine') == False:
	os.mkdir("lyric_machine")

# the algorithm

def the_big_function(singer, song):
	global quickswitch, error_arg1, error_arg2, error_arg3, error_arg4

	# input formatting

	song_clean = re.sub("[^a-z0-9A-Z]", '', song).lower()
	singer_clean = re.sub("[^a-z0-9A-Z]", '', singer).lower()

	if path.exists('lyric_machine/' + singer_clean) == False:
		if quickswitch != 'n':
			os.mkdir("lyric_machine/" + singer_clean)

	# the path concatenation

	the_lyric_path = 'lyric_machine/' + singer_clean + '/' + singer_clean + ' -- ' + song_clean + '.txt'

	# lyrics were saved previously? type it out and exit
	if path.exists(the_lyric_path) == True:
		if quickswitch != 'packet':
			with open(the_lyric_path, 'r') as f:
				data = f.read()
				print(data)
				exit(0)
		else:
			print("Lyrics file already exists.")
			return

	# connections

	url = 'https://www.azlyrics.com/lyrics/' + singer_clean + '/' + song_clean + '.html'

	try:
	    conn = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
	    print('HTTPError: {}'.format(e.code))
	    print(singer, song)
	    print("Page not found. Trying genius.com now....")
	    genius_test(singer, song)
	    if quickswitch != 'packet':
	    	exit(2)
	    else:
	    	return
		    
	except urllib.error.URLError as e:
	    print('URLError: {}'.format(e.reason))
	    print(singer, song)
	    print("Page not found. Trying genius.com now....")
	    genius_test(singer, song)
	    if quickswitch != 'packet':
	    	exit(2)
	    else:
	    	return
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

	# cleanup

	head2, sep2, tail2 = text.partition('" lyrics\n')
	head, sep, tail = tail2.partition('\nSubmit Corrections')
	# unwanted word removal
	head3, sep3, tail3 = head.partition(' Lyrics')
	# concatenation to get clear output
	head = head3 + tail3

	# save or not?

	def output_print(output_switch):
		if output_switch != 'clear':
			print(head)

	def keep_output():
		with open(the_lyric_path, 'w', encoding='utf8') as clear_out_file:
			clear_out_file.write(head)

	def switch_ask(arg):
		while arg not in switches:
			arg = input("Keep lyrics as a text file? (y/n): ").lower()
		switch_check(arg)

	def switch_check(arg):
		if arg != 'n':
			keep_output()
			exit(0)

	if quickswitch == 'packet':
		keep_output()
	else:
		output_print(quickswitch)
		switch_ask(quickswitch)


def flag_eliminator(arg):
	n1, n2, n3 = arg.partition(" ")
	n4, n5, n6 = n3.partition(" ")
	new_line = n1 + n2 + n4
	return new_line

def packet_creator():
	all_lines = 'ignore'
	new_line = ''
	while True:
		new_line = flag_eliminator(input("Pass singer and song: "))
		if new_line != 'done':
			if all_lines == 'ignore':
				all_lines = new_line
			else:
				all_lines = all_lines + '\n' + new_line
		else:
			with open('packet.txt', 'w', encoding='utf8') as p:
				p.write(all_lines)
			exit(0)



if len(sys.argv) > 4: # 5 up
	print(error_arg2)
	exit(1)
else:
	if len(sys.argv) > 3: # 4 args
		if sys.argv[3].lower() in switches:
			singer = sys.argv[1]
			song = sys.argv[2]
			quickswitch = sys.argv[3].lower()
			the_big_function(singer, song)
		else:
			print(error_arg2)
			exit(1)
	else:
		if len(sys.argv) > 2: # 3 args
			if sys.argv[1].lower() == 'packet.txt' and sys.argv[2].lower() == 'packet':
				the_packet = 'packet.txt'
				quickswitch = 'packet'
			else:
				singer = sys.argv[1]
				song = sys.argv[2]
				the_big_function(singer, song)
		else:
			if len(sys.argv) > 1: # 2 args
				if sys.argv[1] == 'help':
					print('\nWELCOME TO LYRIC MACHINE\n\n######## HELP ########\nPass singer and song name. You may use quotes (if name contains spaces), apostrophes, and any case.\nPerfect example if in doubt: acdc highwaytohell\nThe program will make a separate folder in your current directory for outputs.\n\n###### SWITCHES ######\nUse them as a third argument:\nN for no-save, console output;\nY for save, console output;\nCLEAR for save, no console output;\n\n####### PACKET #######\nPacket lyrics download now supported.\nAdd "packet.txt" file in current directory with desired names.\nYou can create packet.txt by passing "packet" as an only argument -- once done type "done".\nExample of packet.txt file:\n\nacdc highwaytohell\nkamelot centeroftheuniverse\n\nExecution: "packet.txt" packet\nNOTE: packet feature uses CLEAR switch. All included switches will be eliminated.\nNOTE: Do not include any spaces in the names of song or singer in packet.txt')
					exit(0)
				elif sys.argv[1] == 'packet':
					packet_creator()
				else:
					print(error_arg3)
					exit(1)
			else: # 1 arg (program only)
				print(error_arg1)
				exit(1)

# unpack packet to extract singer and song

if the_packet != 'u':
	with open(the_packet, 'r', encoding='utf8') as p:
		cont = p.readlines()
		for i in range(0, len(cont)):
			raw_string = flag_eliminator(cont[i])
			singer, sep, tail = raw_string.partition(' ')
			song, sep2, tail2 = tail.partition('\n')
			the_big_function(singer, song)
	print("Download Complete.")
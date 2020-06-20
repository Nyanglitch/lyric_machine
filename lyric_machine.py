import os
from sys import argv
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import os.path
from os import path


# print("Pass singer and song name. You may use quotes (if name contains spaces), apostrophes, and any case.\nPerfect example if in doubt: acdc highwaytohell")
file, singer, song = argv
# singer = input("Singer: ")
# song = input("Song name: ")

if singer and song == 'help':
	print('Help: Pass singer and song name. You may use quotes (if name contains spaces), apostrophes, and any case.\nPerfect example if in doubt: acdc highwaytohell\nThe program will make a separate folder in your current directory for outputs.')
	exit()

# make a dir // check an existing dir

if path.exists('lyric_machine') == False:
	os.mkdir("lyric_machine")

# maybe make it a function?

singer_clean = singer.lower()
singer_clean = singer_clean.replace(' ', '')
singer_clean = singer_clean.replace("'", "")
singer_clean = singer_clean.replace("/", "")
song_clean = song.replace(' ', '')
song_clean = song_clean.replace('"', '')
song_clean = song_clean.replace("'", "")
song_clean = song_clean.lower()
# song_filename = song.replace(' ', '_')
song_filename = song.replace('"', '')

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


# adding everything to the text file

out_file = open('messy_output.txt', 'w')
out_file.write(text)
out_file.close()

# cleaning up the output

out_file = open('messy_output.txt', 'r')
clear_out_file = open('lyric_machine/' + singer + ' -- ' + song_filename + '.txt', 'w')

whole_content = ''

cont = out_file.readlines() 
for i in range(0, len(cont)): 
    if(i in range(0, 30)):
        pass
    else: 
        whole_content = whole_content + cont[i]

# cleanup

head, sep, tail = whole_content.partition('Submit Corrections')
clear_out_file.write(head)

remove_lyrics = " Lyrics"
head = head.replace(remove_lyrics, '')

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

save_submit()
import os
from sys import argv
import urllib.request
from bs4 import BeautifulSoup

file, singer, song = argv

# if singer and song == 'help':
# 	print('Help: ')

# song = song.replace('"', '')

url = 'https://www.azlyrics.com/lyrics/' + singer + '/' + song + '.html'
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

# text.readline(range([1, 5]))

# print(text)

# adding everything to the text file

out_file = open('messy_output.txt', 'w')
out_file.write(text)
out_file.close()

# cleaning up the output

out_file = open('messy_output.txt', 'r')
clear_out_file = open(singer + ' -- ' + song + '.txt', 'w')

whole_content = ''

cont = out_file.readlines() 
# type(cont) 
for i in range(0, len(cont)): 
    if(i in range(0, 30)):
        pass
    # elif i == 31:
    # 	beginning, sep, rest = cont[i].partition(' Lyrics')
    # 	whole_content = whole_content + beginning
    else: 
        whole_content = whole_content + cont[i]

# additions

head, sep, tail = whole_content.partition('Submit Corrections')

clear_out_file.write(head)
print(head)

clear_out_file.close()
out_file.close()
os.remove('messy_output.txt')
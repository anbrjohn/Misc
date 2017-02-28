webpage = "http://www.bachcentral.com/midiindexcomplete.html"
prefix = "http://www.bachcentral.com/"

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import wget
import time
import os

def scrape(webpage, extension=".mid", prefix=prefix):
    http = httplib2.Http()
    status, response = http.request(webpage)
    files = []
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href'):
            linkname = link['href']
            if linkname[-len(extension):] == extension:
                files += [linkname]
    return files    
          
def download(files, delay=0):
    total = len(files)
    i = 1
    for file in files:
        filename = prefix+file
        wget.download(filename)
        print("Downloaded", i, "files out of", total)
        i += 1
        time.sleep(delay)


#Go over all files in a folder of a certain format
#This assumes midis have been converted to csv format
#And saved with .csv extension
def getmidis(extension=".csv"):
    midis = [file for file in os.listdir() if file[-4:] == extension]
    info = []
    for file in midis:
        with open(file) as f:
            try:
                text = f.readlines()
                line = text[0]
                line = line.split(", ")
                tempo = int(line[-1])
                voices = int(line[-2])
            except:
                print(file)
        info.append([voices, tempo, file])
    return info


#Narrow down to only files with n number of tracks
def cull(voices)=4:
    file_info = [x for x in info if x[0] == (voices+1)]
    files = [x[-1] for x in file_info]
    print(len(files))
    return files

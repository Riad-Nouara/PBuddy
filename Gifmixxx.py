import os
import requests
import sys
import re
import threading
from bs4 import BeautifulSoup

#How to use :
#Gifmixxx.exe   categoryIndex   maxGifs     path
#fail safe
if len(sys.argv) != 4:

    print('Invalid arguments ({}) instead of 4'.format(len(sys.argv)))
    quit(1)
else:
    cat = int(sys.argv[1])
    maxGifs = int(sys.argv[2])
    dpath = os.getcwd()

#vars
MAXTHREADS = 5
downloads = 0
categories = ['all',
            'anal',
            'bdsm',
            'bowjob',
            'boobs',
            'cumshot',
            'lesbian',
            'threesome',
            'masturbation',
            'gay']

def connect(url):
    res = requests.get(url)
    if res.status_code == 200:
        return BeautifulSoup(res.content, 'html.parser')
    else:
        return None

def download_gif(url, path):
    #already exists ?
    global downloads, maxGifs
    if downloads >= maxGifs:
        return 0
    name = url.split('/')[-1]
    dpath = os.path.join(path, name)
    if os.path.exists(dpath):
        return 0


    download = requests.get(url, stream = True)
    if download.status_code == 200:
        #find the image name

        with open(dpath, 'bw') as f:
            for chunk in download.iter_content(1024):
                f.write(chunk)
            print('Downloaded {} Successfully'.format(name))
        return 1
    else:
        return 0


def mainloop():
    global cat, dpath, maxGifs, downloads

    while True:
        soup = connect("https://gifmixxx.com/{}-gifs".format(categories[cat]))
        if soup:
            #download the image
            link_holder = soup.find('a', {'class':'gif fit'})
            m = re.search(r"url\((.*)\)", link_holder.attrs['style'])
            if m:
                gif_link =  m.group(1)
                #download gif
                downloads += download_gif(gif_link, dpath)
                print('total : ', downloads)
        #break condition
        if (maxGifs > 0):
            if downloads >= maxGifs:
                break

#create threads and run them
threads = []
for t in range(MAXTHREADS):
    t = threading.Thread(target=mainloop)
    threads.append(t)

#start the threads
for t in threads:
    t.start()

for t in threads:
    t.join()

print('Done')
quit(0)

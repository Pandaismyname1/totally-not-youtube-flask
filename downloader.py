from pprint import pprint
from pytube import YouTube
import re

import multiprocessing as mp
from math import ceil
import requests
import sys, os


CHUNK_SIZE = 2**20  # bytes

def searchInCache(url):
    for downloadedFile in os.scandir('cache'):
        if (downloadedFile.name == url.replace('https://www.youtube.com/watch?v=','')+'.webm'):
            return downloadedFile
    if(sum(os.path.getsize(f) for f in os.listdir('cache') if os.path.isfile(f))>3e+8):
        cleanCache()
    return None


def download(url):
    # yt = YouTube(url,on_progress_callback=None)
    # streams = yt.streams.filter(only_audio=True).all()
    # maxAbr = 0
    # selectedStream = None
    # for stream in streams:
    #     abrStr = stream.abr.replace('kbps','')
    #     abr = int(abrStr)
    #     if(abr>maxAbr):
    #         maxAbr = abr
    #         selectedStream = stream
    # pprint(selectedStream)
    # selectedStream.download('cache',filename = url.replace('https://www.youtube.com/watch?v=',''))
    # return yt.title+'.webm'
    yt = YouTube(url)
    streams = yt.streams.filter(only_audio=True).all()
    maxAbr = 0
    selectedStream = None
    for stream in streams:
        abrStr = stream.abr.replace('kbps','')
        abr = int(abrStr)
        if(abr>maxAbr):
            maxAbr = abr
            selectedStream = stream
    filesize = selectedStream.filesize

    ranges = [[selectedStream.url, i * CHUNK_SIZE, (i+1) * CHUNK_SIZE - 1] for i in range(ceil(filesize / CHUNK_SIZE))]
    ranges[-1][2] = None  # Last range must be to the end of file, so it will be marked as None.

    pool = mp.Pool(min(len(ranges), 64))
    chunks = pool.map(download_chunk, ranges)
    with open('cache/'+url.replace('https://www.youtube.com/watch?v=','')+'.webm', 'wb') as outfile:
        for chunk in chunks:
            outfile.write(chunk)

def cleanCache():
    folder = 'cache'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def download_chunk(args):
    url, start, finish = args
    range_string = '{}-'.format(start)

    if finish is not None:
        range_string += str(finish)

    response = requests.get(url, headers={'Range': 'bytes=' + range_string})
    return response.content

def getMeta(url):
    yt = YouTube(url)
    return yt.title, yt.thumbnail_url

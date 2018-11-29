#!/usr/bin/env python3
from search import searchOnYoutube
from downloader import download, searchInCache, getMeta

import cgi
import json

def downloadVideo(videoId):
    if(searchInCache(videoId)):
        print('Found Cached Version Of ' + videoId)
    else:
        download('https://www.youtube.com/watch?v='+videoId)
        print('Downloaded ' + videoId)
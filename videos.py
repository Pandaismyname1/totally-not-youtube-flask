#!/usr/bin/env python3
from search import searchOnYoutube
from downloader import download, searchInCache, getMeta

import cgi
import json

def downloadVideo(query):
    videoId = searchOnYoutube(query)
    if(searchInCache(videoId)):
        print('Found Cached Version Of '+videoId)
    else:
        download(videoId)
        print('Downloaded '+videoId)
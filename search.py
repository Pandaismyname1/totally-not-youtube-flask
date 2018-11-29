import urllib.request
import urllib.parse
import datetime
import utils
import json
import re


def searchOnYoutube(query):
    print('searchOnYoutube ' + str(datetime.datetime.now()))
    query_string = urllib.parse.urlencode({"search_query": query})
    requestUrl = 'http://www.googleapis.com/youtube/v3/search?'
    parameters = list()
    parameters.append(("part", "snippet"))
    parameters.append(("maxResults", "25"))
    parameters.append(("type", "video"))
    parameters.append(("q", query))
    parameters.append(("key", getYoutubeApiKey()))
    requestUrl += utils.listToParams(parameters)
    print(requestUrl)
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    jsonText = urllib.request.urlopen(urllib.request.Request(requestUrl, headers=hdr)).read()
    print(jsonText)
    jsonObj = json.loads(json)
    videos = extractDataFromJson(jsonObj)
    print('search ' + str(datetime.datetime.now()))
    return "https://www.youtube.com/watch?v=" + videos[0]


def searchInHTML(html):
    results = []
    query = 'href=\"/watch?v=xxxxxxxxxxx\"'
    currentResult = ''
    currentResultPosition = 0
    for chr in html:
        if (len(query) - 14 <= currentResultPosition and currentResultPosition < len(query) - 1) or (
                currentResultPosition < len(query) - 14 and chr == query[currentResultPosition]):
            currentResult += chr
            currentResultPosition += 1
            if currentResultPosition == len(query) - 1:
                results.append(currentResult[-11:])
                currentResult = ''
                currentResultPosition = 0
        else:
            currentResult = ''
            currentResultPosition = 0
    print(results)
    return results


def extractDataFromJson(jsonObj):
    results = []
    for item in jsonObj['items']:
        results.append((jsonObj['item']['id']['videoId'], jsonObj['item']['snippet']['title'],
                        jsonObj['item']['snippet']['thumbnails']['medium']['url']))
    return results


def getYoutubeApiKey():
    with open('../youtubeCredentials.txt', 'r') as f:
        return f.read()

import urllib.parse
def extractVideoID(url):
    return url.replace('https://www.youtube.com/watch?v=', '')


def listToParams(li):
    urlParams = ''
    for index in range(len(li)):
        # if index != 0:
        urlParams += '&'
        urlParams += urllib.parse.quote(li[index][0])+'='+urllib.parse.quote(li[index][1])
    return urlParams

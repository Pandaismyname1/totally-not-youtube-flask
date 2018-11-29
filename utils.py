def extractVideoID(url):
    return url.replace('https://www.youtube.com/watch?v=', '')


def listToParams(li):
    urlParams = ''
    for index in range(len(li)):
        if index != 0:
            urlParams += '&'
        urlParams += li[index][0]+'='+li[index][1]
    return urlParams

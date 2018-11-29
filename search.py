import urllib.request
import urllib.parse
import re
def searchOnYoutube(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    # search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    search_results = searchInHTML(html_content.read().decode())
    return "https://www.youtube.com/watch?v=" + search_results[0]
def searchInHTML(html):
    results = []
    query = 'href=\"/watch?v=xxxxxxxxxxx\"'
    currentResult = ''
    currentResultPosition = 0
    for chr in html:
        if (len(query)-14 <= currentResultPosition and currentResultPosition < len(query)-1) or (currentResultPosition<len(query)-14 and chr == query[currentResultPosition]):
            currentResult += chr
            currentResultPosition += 1
            if currentResultPosition==len(query)-1:
                results.append(currentResult[-11:])
                currentResult = ''
                currentResultPosition = 0
        else:
            currentResult = ''
            currentResultPosition = 0
    print(results)
    return results
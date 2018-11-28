from flask import Flask, request,redirect,send_from_directory
import json
import videos,utils, downloader, json
#
app = Flask(__name__)


@app.route('/')
def player():
    return send_from_directory('front', 'player.html')


@app.route('/resource/<resource>')
def resource(resource):
    return send_from_directory('front', resource)


@app.route('/requestVideo')
def requestVideo():
    req = request.args['videoUrl']
    videos.downloadVideo(req)
    print(req)
    meta = downloader.getMeta("https://www.youtube.com/watch?v=" +req)
    print(meta)
    return json.dumps(('cache?videoId='+utils.extractVideoID(req),meta[0],meta[1]))


@app.route('/searchVideo')
def searchVideo():
    req = request.args['query']
    return redirect('requestVideo?videoUrl='+utils.extractVideoID(videos.searchOnYoutube(req)))


@app.route('/cache')
def cache():
    req = request.args['videoId']
    return send_from_directory('cache',req+'.webm')


if __name__ == '__main__':
    app.run()

    

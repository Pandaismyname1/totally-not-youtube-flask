//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Global Vars
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
var queue = [];
var queueIndex = 0;


//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Application
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function init() {
    document.getElementById('audioPlayer').addEventListener('ended', onSongEnded);
}

function queueEntry(link, title, author, thumbnail)
{
    this.link = link;
    this.title = title;
    this.author = author;
    this.thumbnail = thumbnail;
}

function request(parameters,destination,callback)
{
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", destination+objToUrlParams(parameters));
    xmlhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200)
        {
            callback(this.response);
        }
    };
    // xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlhttp.send();
}

function objToUrlParams(obj)
{
    var str = "";
    for (var key in obj) {
        if (str !== "") {
            str += "&";
        }
        str += key + "=" + encodeURIComponent(obj[key]);
    }
    return str
}

function search() {
    var obj = {}
    obj['query'] = document.getElementById('searchInput').value;
    request(obj,'/searchVideo?', searchCallback)
}

function searchCallback(url) {
    let newSong = new queueEntry(url, null, null, null);
    queue.push(newSong)
}

function playSong(url) {
    document.getElementById('audioPlayerSource').src = url;
    document.getElementById('audioPlayer').load();
    document.getElementById('audioPlayer').play();
}

function playNextSong() {
    queueIndex += 1;
    if(queueIndex>=queue.length)
    {
        queueIndex=0;
    }
    playSong(queue[queueIndex]);
}

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// UI
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function onPlayButtonPressed() {
    playSong(queue[0]);
}

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Handlers
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function onSongEnded() {
    playNextSong();
}
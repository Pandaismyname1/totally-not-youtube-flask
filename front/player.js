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
    playSong(queue[queueIndex].link);
}

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// API Callbacks
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function searchCallback(url) {
    let newSong = new queueEntry(url, null, null, null);
    queue.push(newSong);
    addQueueEntryUI(newSong);
    console.log(queue);
    console.log(newSong);
    console.log(url)
}

function addQueueEntryUI(queueEntry)
{
    queueContainer = document.getElementById('queueContainer');

    var queueEntryContainer = document.createElement('div');
    queueEntryContainer.id = 'queueEntryContainer' +queueEntry.link;
    queueEntryContainer.style.height = '5em';
    queueEntryContainer.style.width = '24em';
    queueEntryContainer.style.padding = '0.5em';

    var queueEntryThumbnail = document.createElement('div');
    queueEntryThumbnail.id = 'queueEntryThumbnail' +queueEntry.link;
    queueEntryThumbnail.className = 'queueEntryThumbnail'
    queueEntryThumbnail.style.height = '5em';
    queueEntryThumbnail.style.width = '24em';
    queueEntryThumbnail.style.cssFloat = 'left';
    queueEntryThumbnail.style.backgroundImage = 'url(/thumbnails/'+queueEntry.thumbnail+')';

    var queueEntryTitle = document.createElement('p');
    queueEntryTitle.id = 'queueEntryTitle' +queueEntry.link;
    queueEntryTitle.className = 'queueEntryTitle';
    queueEntryTitle.innerHTML = queueEntry.title;
    queueEntryTitle.style.width = '15em';
    queueEntryTitle.style.cssFloat = 'left';

    var queueEntryPlay = document.createElement('button');
    queueEntryPlay.id = 'queueEntryPlay' +queueEntry.link;
    queueEntryPlay.className = 'queueEntryPlay';
    queueEntryPlay.innerText = 'Play';
    queueEntryPlay.style.bottom = '-2em';
    queueEntryPlay.style.position = 'relative';
    queueEntryPlay.style.cssFloat = 'left';

    queueEntryContainer.appendChild(queueEntryThumbnail);
    queueEntryContainer.appendChild(queueEntryTitle);
    queueEntryContainer.appendChild(queueEntryPlay);
    queueContainer.appendChild(queueEntryContainer);
}

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// UI
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function onPlayButtonPressed() {
    playSong(queue[0].link);
}

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Handlers
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function onSongEnded() {
    playNextSong();
}
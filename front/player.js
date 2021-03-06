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

function queueEntry(link, title, thumbnail)
{
    this.link = link;
    this.title = title;
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

function playSong(queueEntry) {
    document.getElementById('playerInfoSongName').innerHTML = queueEntry.title;
    document.getElementById('playerInfoSongUrl').innerHTML = 'https://www.youtube.com/watch?v='+queueEntry.link.toString().replace('cache?videoId=','');
    document.getElementById('audioPlayerSource').src = queueEntry.link;
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

function playPreviousSong() {
    queueIndex -= 1;
    if(queueIndex<0)
    {
        queueIndex=queue.length-1;
    }
    playSong(queue[queueIndex]);
}


//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// API Callbacks
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function searchCallback(json) {
    jsonObj = JSON.parse(json)
    let newSong = new queueEntry(jsonObj[0], jsonObj[1], jsonObj[2]);
    queue.push(newSong);
    addQueueEntryUI(newSong);
    console.log(queue);
    console.log(newSong);
    console.log(json)
}

function addQueueEntryUI(queueEntry)
{
    queueContainer = document.getElementById('queueContainer');

    var queueEntryContainer = document.createElement('div');
    queueEntryContainer.className = 'queueEntryContainer'
    queueEntryContainer.id = 'queueEntryContainer' +queueEntry.link;

    var queueEntryThumbnail = document.createElement('div');
    queueEntryThumbnail.id = 'queueEntryThumbnail' +queueEntry.link;
    queueEntryThumbnail.className = 'queueEntryThumbnail'
    queueEntryThumbnail.style.backgroundImage = 'url('+queueEntry.thumbnail+')';

    var queueEntryTitle = document.createElement('p');
    queueEntryTitle.id = 'queueEntryTitle' +queueEntry.link;
    queueEntryTitle.className = 'queueEntryTitle';
    queueEntryTitle.innerHTML = queueEntry.title;

    var queueEntryPlay = document.createElement('div');
    queueEntryPlay.id = 'queueEntryPlay' +queueEntry.link;
    queueEntryPlay.className = 'queueEntryPlay';
    var queuePosition = queue.length - 1;
    queueEntryPlay.addEventListener('click', function() { playSongInQueue(queuePosition); } );

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
function onNextButtonPressed() {
    playNextSong();
}
function onPreviousButtonPressed() {
    playPreviousSong(queue[0]);
}

function playSongInQueue(index) {
    queueIndex = index
    playSong(queue[index]);
}

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Handlers
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function onSongEnded() {
    playNextSong();
}
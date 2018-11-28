function request(parameters,destination,callback)
{
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", destination+objToUrlParams(parameters));
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
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
        if (str != "") {
            str += "&";
        }
        str += key + "=" + encodeURIComponent(obj[key]);
    }
    return str
}
function search() {
    var obj = {}
    var query = document.getElementById('searchInput').value
    obj['query'] = query
    request(obj,'/searchVideo?', searchCallback)
}
function searchCallback(url) {
    document.getElementById('audioPlayerSource').src = url;
    document.getElementById('audioPlayer').load();
    document.getElementById('audioPlayer').play();
}
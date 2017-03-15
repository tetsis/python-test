//let stadiums;
//let games;

function getStadiums(afterFunction) {
    let hostname = window.location.hostname;
    let port = window.location.port;
    let url = 'http://' + hostname + ':' + port + '/api/stadiums/?format=json';
    let xhr = XMLHttpRequestCreate();
    xhr.open("GET", url);
    xhr.responseType = "json";
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState == 4) {
            if (Math.floor(xhr.status/100) == 2) {
                console.log("GET success");
                stadiums = xhr.response;
                console.log(stadiums);
            }
            else {
                console.log("Error");
            }
            afterFunction();
        }
    }
    xhr.send();
}

function getGames(afterFunction) {
    let hostname = window.location.hostname;
    let port = window.location.port;
    let url = 'http://' + hostname + ':' + port + '/api/games/?format=json';
    let xhr = XMLHttpRequestCreate();
    xhr.open("GET" , url);
    xhr.responseType = "json";
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState == 4) {
            if (Math.floor(xhr.status/100) == 2) {
                console.log("GET success");
                games = xhr.response;
                console.log(games);
            }
            else {
                console.log("Error");
            }
            afterFunction();
        }
    }
    xhr.send();
}

function XMLHttpRequestCreate(){
    try{
        return new XMLHttpRequest();
    }catch(e){}
    try{
        return new ActiveXObject('MSXML2.XMLHTTP.6.0');
    }catch(e){}
    try{
        return new ActiveXObject('MSXML2.XMLHTTP.3.0');
    }catch(e){}
    try{
        return new ActiveXObject('MSXML2.XMLHTTP');
    }catch(e){}

    return null;
}

function getCookie( name )
{
    var result = null;

    var cookieName = name + '=';
    var allcookies = document.cookie;

    var position = allcookies.indexOf( cookieName );
    if( position != -1 )
    {
        var startIndex = position + cookieName.length;

        var endIndex = allcookies.indexOf( ';', startIndex );
        if( endIndex == -1 )
        {
            endIndex = allcookies.length;
        }

        result = decodeURIComponent(
                allcookies.substring( startIndex, endIndex ) );
    }

    return result;
}

function getCSV(data) {
    let result = new Array();
    let lines = new Array();
    lines = data.split('\n');
    for (let i = 0; i < lines.length; i++) {
        lines[i] = lines[i].replace('\r', '');
        let cells = lines[i].split(',');
        result.push(cells);
    }
    return result;
}

function getXLSX(data) {
    console.log('getXLSX');
    console.log(data);
}

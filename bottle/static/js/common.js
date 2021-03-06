//プレイヤーIDからプレイヤー名を取得
function getPlayer(id) {
    for (var i = 0; i < playerArray.length; i++) {
        if (playerArray[i].id == id) {
            return playerArray[i];
        }
    }

    return null;
}

//GET
function getFromAPI(api, afterFunction) {
    let url = api;
    let xhr = XMLHttpRequestCreate();
    xhr.open("GET", url);
    xhr.responseType = "json";
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.response);
            afterFunction(xhr.status, xhr.response);
        }
    }
    xhr.send();
}

//POST
function postToAPI(api, data, afterFunction) {
    let url = api;
    let xhr = XMLHttpRequestCreate();
    data = JSON.stringify(data);
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    //xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
            //header = xhr.getResponseHeader("Set-Cookie");
            //console.log(header);
            afterFunction(xhr.status, xhr.responseText);
        }
    }
    xhr.send(data);
}

//DELETE
function deleteFromAPI(api, afterFunction) {
    let url = api;
    let xhr = XMLHttpRequestCreate();
    xhr.open("DELETE", url);
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState === 4) {
            console.log(xhr.status);
            afterFunction(xhr.status);
        }
    }
    xhr.send();
}

function XMLHttpRequestCreate(){
    try {
        return new XMLHttpRequest();
    }
    catch(e) {}
    try {
        return new ActiveXObject('MSXML2.XMLHTTP.6.0');
    }
    catch(e) {}
    try {
        return new ActiveXObject('MSXML2.XMLHTTP.3.0');
    }
    catch(e) {}
    try {
        return new ActiveXObject('MSXML2.XMLHTTP');
    }
    catch(e){}

    return null;
}

function getCookie(name)
{
    let result = null;
    let cookieName = name + '=';
    let allcookies = document.cookie;

    let position = allcookies.indexOf(cookieName);
    if (position != -1)
    {
        let startIndex = position + cookieName.length;

        let endIndex = allcookies.indexOf(';', startIndex);
        if (endIndex == -1)
        {
            endIndex = allcookies.length;
        }

        result = decodeURIComponent(allcookies.substring(startIndex, endIndex));
    }
    return result;
}

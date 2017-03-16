
//GET
function getFromAPI(api, afterFunction) {
    let url = api + '/?format=json';
    let xhr = XMLHttpRequestCreate();
    xhr.open("GET", url);
    xhr.responseType = "json";
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState === 4) {
            //console.log(xhr.response);
            if (Math.floor(xhr.status/100) === 2) {
                //console.log("GET Success");
                //console.log(xhr.response);
            }
            else {
                //console.log("GET Error");
            }
            afterFunction(xhr.response);
        }
    }
    xhr.send();
}

//POST
function postToAPI(api, afterFunction) {
    let url = api;
    let xhr = XMLHttpRequestCreate();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    //xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState === 4) {
            //console.log(xhr.responseText);
            if (Math.floor(xhr.status/100) === 2) {
                //console.log("POST Success");
                //console.log(xhr.responseText);
            }
            else {
                //console.log("POST Error");
                //console.log(xhr.responseText);
            }
            afterFunction(xhr.responseText);
        }
    }
    xhr.send(data);
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


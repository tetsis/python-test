window.addEventListener('load',
    function (event) {
        document.getElementById('btn_get').addEventListener('click',
            function() {
                getFromAPI('http://127.0.0.1:8000/api', afterGet);
            }
        , false);
        document.getElementById('btn_post').addEventListener('click', clickPost, false);
    }
, false);

function afterGet(response) {
    console.log(response);
}

function afterPost(responseText) {
    console.log(responseText);
}

function clickPost() {
    let villageName = document.getElementById('ipt_villageName').value;
    let data = {
        name: villageName
    };
    postToAPI('http://127.0.0.1:8000/api/tables/', data, afterPost);
}

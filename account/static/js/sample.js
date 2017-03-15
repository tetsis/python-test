window.addEventListener('load',
    function (event) {
        document.getElementById('button').addEventListener('click',
            function() {
            alert('Hello');
            }
            , false);
        document.getElementById('submit').addEventListener('click', clickSubmit, false);
    }
    , false);


function clickSubmit() {
}

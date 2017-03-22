window.addEventListener('load',
    function (event) {
        getVillages();
        document.getElementById('btn_update').addEventListener('click', clickUpdate, false);
        document.getElementById('btn_participate').addEventListener('click', clickParticipate, false);
    }
, false);

function setVillages(response) {
    let slc_villages = document.getElementById('slc_villages');
    let villagesArray = response;
    slc_villages.textContent = null;

    for (let i = 0; i < villagesArray.length; i++) {
        let opt_village = document.createElement('option');
        opt_village.value = villagesArray[i].id;
        opt_village.innerHTML = villagesArray[i].name;
        slc_villages.appendChild(opt_village);
    }
}

function clickUpdate() {
    getVillages();
}

function clickParticipate() {
    let slc_villages = document.getElementById('slc_villages');
    let selectedVillage = slc_villages.selectedIndex;

    console.log(selectedVillage);
    postToAPI('http://127.0.0.1:8000/api/village/' + selectedVillage + '/');
}

function getVillages() {
    getFromAPI('http://127.0.0.1:8000/api/villages/', setVillages);
}

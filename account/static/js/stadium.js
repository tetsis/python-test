let stadiums;
window.addEventListener('load',
    function (event) {
        getStadiums(drawStadiums);
        document.getElementById('btnPlus').addEventListener('click', clickPlus, false);
        document.getElementById('iptImport').addEventListener('change', changeIptImport, false);
        document.getElementById('iptImport').style.display = 'none';
        document.getElementById('btnImport').addEventListener('click', clickImport, false);
        document.getElementById('btnExport').addEventListener('click', clickExport, false);
        document.getElementById('btnAdd').addEventListener('click', clickAdd, false);
        document.getElementById('btnUpdate').addEventListener('click', clickUpdate, false);
        document.getElementById('btnDelete').addEventListener('click', clickDelete, false);
    }
, false);

function clickPlus() {
    document.getElementById('btnAdd').style.display = 'inline';
    document.getElementById('btnUpdate').style.display = 'none';
    document.getElementById('btnDelete').style.display = 'none';
    document.getElementById('iptId').value = '';
    document.getElementById('iptStadiumId').value = '';
    document.getElementById('iptName').value = '';
    document.getElementById('iptCodeName').value = '';
    document.getElementById('iptAddress').value = '';
    document.getElementById('iptContact').value = '';
    $('#mdlStadium').modal('show');
}

function clickEdit(obj) {
    let tr = obj.parentNode.parentNode;
    let id = tr.childNodes[0].value;
    let stadiumId = tr.childNodes[1].innerHTML;
    let name = tr.childNodes[2].innerHTML;
    let codeName = tr.childNodes[3].innerHTML;
    let address = tr.childNodes[4].innerHTML;
    let contact = tr.childNodes[5].innerHTML;
    document.getElementById('btnAdd').style.display = 'none';
    document.getElementById('btnUpdate').style.display = 'inline';
    document.getElementById('btnDelete').style.display = 'inline';
    document.getElementById('iptId').value = id;
    document.getElementById('iptStadiumId').value = stadiumId;
    document.getElementById('iptName').value = name;
    document.getElementById('iptCodeName').value = codeName;
    document.getElementById('iptAddress').value = address;
    document.getElementById('iptContact').value = contact;
    $('#mdlStadium').modal('show');
}

function clickAdd() {
    let stadiumId = document.getElementById('iptStadiumId').value;
    let name = document.getElementById('iptName').value;
    let codeName = document.getElementById('iptCodeName').value;
    let address = document.getElementById('iptAddress').value;
    let contact = document.getElementById('iptContact').value;
    let data = {
        stadium_id: stadiumId,
        name: name,
        code_name: codeName,
        address: address,
        contact: contact
    };
    let hostname = window.location.hostname;
    let port = window.location.port;
    let url = 'http://' + hostname + ':' + port + '/api/stadiums/';
    let xhr = XMLHttpRequestCreate();
    data = JSON.stringify(data);
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState == 4) {
            if (Math.floor(xhr.status/100) == 2) {
                console.log("Success");
                location.reload();
                //console.log(xhr.responseText);
            }
            else {
                console.log("Error");
                //console.log(xhr.responseText);
            }
        }
    }
    xhr.send(data);
    $('#mdlStadium').modal('hide');
}

function clickImport() {
    let file = document.getElementById('iptImport');
    file.click();
}

function changeIptImport(event) {
    let file = event.target.files[0];
    let render = new FileReader();

    render.onload = function(event) {
        let result = getCSV(event.target.result);
        if (result !== null) {
            for (let i = 0; i < result.length; i++) {
                let data = {
                    stadium_id: result[i][0],
                    name: result[i][1],
                    code_name: result[i][2],
                    address: result[i][3],
                    contact: result[i][4]
                };
                let hostname = window.location.hostname;
                let port = window.location.port;
                let url = 'http://' + hostname + ':' + port + '/api/stadiums/';
                let xhr = XMLHttpRequestCreate();
                data = JSON.stringify(data);
                xhr.open("POST", url, false);
                xhr.setRequestHeader("Content-Type", "application/json");
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                xhr.onreadystatechange = function(event) {
                    if (xhr.readyState == 4) {
                        if (Math.floor(xhr.status/100) == 2) {
                            console.log("Success");
                            //console.log(xhr.responseText);
                        }
                        else {
                            console.log("Error");
                            //console.log(xhr.responseText);
                        }
                    }
                }
                xhr.send(data);
            }
            location.reload();
        }
    }
    render.readAsText(file, "Shift_JIS");
}

function clickExport() {
    let bom = new Uint8Array([0xEF, 0xBB, 0xBF]);
    let content = '';
    for (let i = 0; i < stadiums.length; i++) {
        content += stadiums[i].stadium_id + ',' + stadiums[i].name + ',' + stadiums[i].code_name + ',' + stadiums[i].address + ',' + stadiums[i].contact + '\n';
    }
    let blob = new Blob([ bom, content ], { "type" : "text/csv" });

    aExport = document.getElementById('aExport');
    aExport.href = window.URL.createObjectURL(blob);
    aExport.click();
}

function clickUpdate() {
    let id = document.getElementById('iptId').value;
    let stadiumId = document.getElementById('iptStadiumId').value;
    let name = document.getElementById('iptName').value;
    let codeName = document.getElementById('iptCodeName').value;
    let address = document.getElementById('iptAddress').value;
    let contact = document.getElementById('iptContact').value;
    let data = {
        stadium_id: stadiumId,
        name: name,
        code_name: codeName,
        address: address,
        contact: contact
    };
    let hostname = window.location.hostname;
    let port = window.location.port;
    let url = 'http://' + hostname + ':' + port + '/api/stadiums/' + id + '/';
    let xhr = XMLHttpRequestCreate();
    data = JSON.stringify(data);
    xhr.open("PUT", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState == 4) {
            if (Math.floor(xhr.status/100) == 2) {
                console.log("Success");
                location.reload();
                //getStadiums();
                //console.log(xhr.responseText);
            }
            else {
                console.log("Error");
                //console.log(xhr.responseText);
            }
        }
    }
    xhr.send(data);
    $('#mdlStadium').modal('hide');
}

function clickDelete() {
    let id = document.getElementById('iptId').value;
    let hostname = window.location.hostname;
    let port = window.location.port;
    let url = 'http://' + hostname + ':' + port + '/api/stadiums/' + id + '/';
    let xhr = XMLHttpRequestCreate();
    xhr.open("DELETE", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.onreadystatechange = function(event) {
        if (xhr.readyState == 4) {
            if (Math.floor(xhr.status/100) == 2) {
                console.log("Success");
                location.reload();
                //console.log(xhr.responseText);
            }
            else {
                console.log("Error");
                //console.log(xhr.responseText);
            }
        }
    }
    xhr.send();
    $('#mdlStadium').modal('hide');
}

function drawStadiums() {
    let tbStadium = document.getElementById('tbStadium');
    tbStadium.textContent = null;
    for (let i = 0; i < stadiums.length; i++) {
        let tr = document.createElement('tr');
        let iptId = document.createElement('input');
        let tdStadiumId = document.createElement('td');
        let tdName = document.createElement('td');
        let tdCodeName = document.createElement('td');
        let tdAddress = document.createElement('td');
        let tdContact = document.createElement('td');
        let tdEdit = document.createElement('td');
        let btnEdit = document.createElement('button');
        iptId.type = 'hidden';
        iptId.value = stadiums[i].id;
        tdStadiumId.innerHTML = stadiums[i].stadium_id;
        tdName.innerHTML = stadiums[i].name;
        tdCodeName.innerHTML = stadiums[i].code_name;
        tdAddress.innerHTML = stadiums[i].address;
        tdContact.innerHTML = stadiums[i].contact;
        btnEdit.type = 'button';
        btnEdit.className = 'btn btn-primary btn-xs';
        btnEdit.innerHTML = 'edit';
        btnEdit.addEventListener('click', function(){clickEdit(this)}, false);
        tdEdit.appendChild(btnEdit);
        tr.appendChild(iptId);
        tr.appendChild(tdStadiumId);
        tr.appendChild(tdName);
        tr.appendChild(tdCodeName);
        tr.appendChild(tdAddress);
        tr.appendChild(tdContact);
        tr.appendChild(tdEdit);
        tbStadium.appendChild(tr);
    }
    $('#tblStadium').DataTable();
}

/*!
    * Start Bootstrap - SB Admin v7.0.5 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2022 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function editForm(id) {
    document.getElementById('view-table-' + id).style.display = 'none';
    document.getElementById('edit-form-' + id).style.display = 'block';
    document.getElementById('edit-button-' + id).style.display = 'none';
    document.getElementById('save-button-' + id).style.display = 'block';
}

function getCsrfToken() {
    const csrfElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfElement.value;
}

function updateTable(id, data) {
    const table = document.getElementById('view-table-' + id);
    const rows = table.rows;

    rows[0].cells[1].textContent = data.auth_name;
    rows[1].cells[1].textContent = data.mspid;
    rows[2].cells[1].textContent = data.cryptopath;
    rows[3].cells[1].textContent = data.certpath;
    rows[4].cells[1].textContent = data.keypath;
    rows[5].cells[1].textContent = data.tlscertpath;
    rows[6].cells[1].textContent = data.peerendpoint;
    rows[7].cells[1].textContent = data.gatewaypeer;
}

async function submitForm(id) {
    const form = document.getElementById('edit-form-' + id);
    const formData = new FormData(form);

    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    try { 
        const response = await fetch(`/updateAuthenticationPeer/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), 
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // 데이터가 성공적으로 업데이트되면 모달을 닫고 원래 텍스트 테이블로 돌아갑니다.
            const updatedData = await response.json();
            updateTable(id, updatedData);

            const modal = bootstrap.Modal.getInstance(document.getElementById('exampleModal' + id));
            modal.hide();
        } else {
            // 에러 처리
            console.error('Error updating data:', response);
        }
    } catch (error) {
        console.error('Error in submitForm():', error);
    }
}

function checkAuthentication(auth_peer_id) {
    var request = new XMLHttpRequest();
    request.open('get', '/client_hlf/' + auth_peer_id + '/', true); // URL을 기반으로 POST 요청을 엽니다.
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());

    request.onload = function () {
        var response = JSON.parse(request.responseText);
        var card = document.getElementById("card-" + auth_peer_id);
        console.info(response);
        if (response === 200) { // 성공 시에는 bg-primary 클래스를 추가하고 bg-error 클래스를 제거합니다.
            card.classList.add('bg-primary');
            card.classList.remove('bg-danger');
        } else { // 실패 시에는 bg-error 클래스를 추가하고 bg-primary 클래스를 제거합니다.
            card.classList.add('bg-danger');
            card.classList.remove('bg-primary');
        }
    };

    request.onerror = function () {
        console.error("Error: failed to send authentication request");
    };

    request.send(); // 요청을 보냅니다.
}

function checkAllAuthentications(auth_peer_ids) {
    auth_peer_ids.forEach(function(auth_peer_id) {
        checkAuthentication(auth_peer_id);
    });
}

function initAuthentications() {
    const auth_peer_ids = JSON.parse(document.getElementById('auth_peer_ids').textContent);
    checkAllAuthentications(auth_peer_ids);
}
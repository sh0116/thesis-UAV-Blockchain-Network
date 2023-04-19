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

    fetchdisplayMissions();
});

async function fetchMissions(authId, MissionFuction) {
    try {
        const response = await fetch(`/hlf_getAllMission/${authId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
        });

        if (response.ok) {
            const missions = await response.json();
            displayMissions(missions, MissionFuction);
        } else {
            console.error('Error fetching missions:', response);
        }
    } catch (error) {
        console.error('Error in fetchMissions():', error);
    }
}

function displayMissions(missions, MissionFuction) {
    const missionCardsContainer = document.getElementById('mission-cards').querySelector('.row');

    missions.forEach(mission => {
        const colDiv = document.createElement('div');
        colDiv.classList.add('col-xl-12', 'col-md-6');

        const cardDiv = document.createElement('div');
        cardDiv.classList.add('card', 'text-white', 'mb-4', 'bg-primary');
        cardDiv.id = `card-${mission.id}`;

        const cardBodyDiv = document.createElement('div');
        cardBodyDiv.classList.add('card-body');

        const cardTitle = document.createElement('h5');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = mission.id;

        const cardText = document.createElement('p');
        cardText.classList.add('card-text');
        cardText.textContent = mission.comments;

        const cardFooterDiv = document.createElement('div');
        cardFooterDiv.classList.add('card-footer', 'd-flex', 'align-items-center', 'justify-content-between');

        const footerText = document.createElement('span')

        const checkMark = document.createElement('i');
        checkMark.classList.add('fas', 'fa-check', 'text-success', 'd-none');
        checkMark.style.position = 'absolute';
        checkMark.style.top = '10px';
        checkMark.style.right = '10px';
        
        if (MissionFuction==="select") {
            cardDiv.onclick = () => MissionselectMissionSelCard(`card-${mission.id}`);
        } else if (MissionFuction==="delete"){
            cardDiv.onclick = () => MissionselectMissionDelCard(`card-${mission.id}`);
        }
        


        cardBodyDiv.appendChild(checkMark);
        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText);
        cardFooterDiv.appendChild(footerText);
        cardDiv.appendChild(cardBodyDiv);
        cardDiv.appendChild(cardFooterDiv);
        colDiv.appendChild(cardDiv);
        missionCardsContainer.appendChild(colDiv);
    });
}

function deselectAllCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.remove('border-warning');
        const checkMark = card.querySelector('.fa-check');
        if (checkMark) {
            checkMark.classList.add('d-none');
        }
    });
}

function MissionselectMissionSelCard(cardId) {
    const card = document.getElementById(cardId);
    const checkMark = card.querySelector('.fa-check');

    if (card.classList.contains('border-warning')) {
        card.classList.remove('border-warning');
        checkMark.classList.add('d-none');
    } else {
        deselectAllCards();
        card.classList.add('border-warning');
        checkMark.classList.remove('d-none');

        selectedMissionId = cardId.replace('card-', '');
        document.getElementById('task-container').style.display = 'block';
    }
}

function MissionselectMissionDelCard(cardId) {
    const card = document.getElementById(cardId);
    const checkMark = card.querySelector('.fa-check');

    if (card.classList.contains('border-warning')) {
        card.classList.remove('border-warning');
        checkMark.classList.add('d-none');
    } else {
        deselectAllCards();
        card.classList.add('border-warning');
        checkMark.classList.remove('d-none');

        selectedMissionId = cardId.replace('card-', '');
        $('#deleteMissionModal').modal('show');
    }
}

async function fetchdisplayMissions() {
    try {
        const response = await fetch(`/hlf_getAllMission/0/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
        });

        if (response.ok) {
            const missions = await response.json();
            displayHomeMissions(missions);
        } else {
            console.error('Error fetching missions:', response);
        }
    } catch (error) {
        console.error('Error in fetchMissions():', error);
    }
}

function updateCurrentSlide(slideIndex) {
    const currentSlideElement = document.getElementById('current-slide');
    currentSlideElement.textContent = slideIndex ;
}

function displayHomeMissions(missions) {
    const missionsContainer = document.getElementById('missions-container');
    const indicatorsContainer = document.getElementById('missions-indicators');

    const missionCount = missions.length;
    const missionCountElement = document.getElementById('mission-count');
    missionCountElement.textContent = missionCount;


    missions.forEach((mission, index) => {
        const indicator = document.createElement('button');
        indicator.type = 'button';
        indicator.setAttribute('data-bs-target', '#missionsCarousel');
        indicator.setAttribute('data-bs-slide-to', index);
        indicator.classList.add('carousel-indicator');
        if (index === 0) {
            indicator.classList.add('active');
        }
        indicatorsContainer.appendChild(indicator);

        // Create carousel item
        const carouselItem = document.createElement('div');
        carouselItem.classList.add('carousel-item');
        carouselItem.setAttribute('data-slide-index', index);
        carouselItem.style.textAlign = 'center';
        
        if (index === 0) {
            carouselItem.classList.add('active');
        }

        const missionCard = document.createElement('div');
        missionCard.classList.add('card', 'shadow', 'h-100', 'py-2');

        const missionCardBody = document.createElement('div');
        missionCardBody.classList.add('card-body');

        const missionTitle = document.createElement('h5');
        missionTitle.classList.add('card-title');
        missionTitle.textContent = mission.id;

        const missionComments = document.createElement('p');
        missionComments.classList.add('card-text');
        missionComments.textContent = mission.comments;

        const missionAssetIDs = document.createElement('ul');
        mission.asset_ids.forEach(assetID => {
            const assetIDItem = document.createElement('li');
            assetIDItem.textContent = assetID;
            missionAssetIDs.appendChild(assetIDItem);
        });

        missionCardBody.appendChild(missionTitle);
        missionCardBody.appendChild(missionComments);
        missionCardBody.appendChild(missionAssetIDs);
        missionCard.appendChild(missionCardBody);
        carouselItem.appendChild(missionCard);
        missionsContainer.appendChild(carouselItem);
    });
    const missionsCarousel = document.getElementById('missionsCarousel');
    missionsCarousel.addEventListener('slid.bs.carousel', (event) => {
        updateCurrentSlide(event.relatedTarget.dataset.slideIndex);
    });
}

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
    request.open('get', '/hlf_Connect/' + auth_peer_id + '/', true); // URL을 기반으로 POST 요청을 엽니다.
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());

    request.onload = function () {
        var response = JSON.parse(request.responseText);
        var card = document.getElementById("card-" + auth_peer_id);
        console.info("response");
        console.info(request);
        if (response !== 500) { // 성공 시에는 bg-primary 클래스를 추가하고 bg-error 클래스를 제거합니다.
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

function MissionselectPeerCard(cardId, authId, MissionFuction) {
    // Clear the previous selection, if any
    const selectedCards = document.querySelectorAll('.card.border-success');
    for (let i = 0; i < selectedCards.length; i++) {
        selectedCards[i].classList.remove('border-success');
        const checkId = selectedCards[i].id.replace('card', 'check');
        document.getElementById(checkId).classList.add('d-none');
    }

    // Set the new selection
    const card = document.getElementById(cardId, authId);
    card.classList.add('border-success');

    const checkId = cardId.replace('card', 'check');
    document.getElementById(checkId).classList.remove('d-none');
    document.getElementById('lower-row').style.display = 'flex';

    fetchMissions(authId, MissionFuction);
}

async function submitMission() {
    const missionId = document.getElementById('mission-id').value;
    const missionComment = document.getElementById('mission-comment').value;

    const selectedCard = document.querySelector('.card.border-success');
    const authId = selectedCard.id.replace('card-', '');

    const postData = {
        Mission_Asset: {
            ID: missionId,
            Comments: missionComment,
            AssetIDs: '',
        },
    };;

    fetch(`/hlf_createMission/${authId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(postData),
    })
    .then((response) => {
        if (response.status!==500) {
            console.log('Mission submitted successfully', response);
            window.location.href = '/';
        } else {
            console.error('Error submitting mission:', response);
            alert('Failed to submit the mission. Please try again.');
            window.location.href = '/';
        }
    })
    .catch((error) => {
        console.error('Error in submitMission():', error);
        alert('Failed to submit the mission. Please try again.');
        window.location.href = '/';
    });
}

async function deleteMission() {
    if (!selectedMissionId) {
        alert('Please select a mission to delete.');
        return;
    }
    const authselectedCard = document.querySelector('.card.border-success');
    const authId = authselectedCard.id.replace('card-', '');
    const postData = {
        Mission_Asset: {
            ID: selectedMissionId,
        },
    };;
    fetch(`/hlf_deleteMission/${authId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(postData),
    })
    .then((response) => {
        if (response.status !== 500) {
            console.log('Mission deleted successfully', response);
            // Redirect to the home page after successful deletion
            window.location.href = '/';
        } else {
            console.error('Error deleting mission:', response);
            alert('Failed to delete the mission. Please try again.');
            // Redirect to the home page after showing the failure alert
            window.location.href = '/';
        }
    })
    .catch((error) => {
        console.error('Error in deleteMission():', error);
        alert('Failed to delete the mission. Please try again.');
        // Redirect to the home page after showing the failure alert
        window.location.href = '/';
    });
}

async function createTask() {
    // Get latitude, longitude, and UAV ID from the form inputs
    const task_id = document.getElementById('task-id-input').value;
    const latitude = document.getElementById('latitude-input').value;
    const longitude = document.getElementById('longitude-input').value;
    const uavName = document.getElementById('inputGroupSelect01').options[document.getElementById('inputGroupSelect01').selectedIndex].text;

    if (!selectedMissionId) {
        alert('Please select a mission to delete.');
        return;
    }
    const authselectedCard = document.querySelector('.card.border-success');
    const authId = authselectedCard.id.replace('card-', '');


    const postData = {
        Task_Asset: {
            ID          : task_id,
            Name        : uavName,
            task_id     : "",
            mission_id  : selectedMissionId,
            Latitude    : latitude,
            Longitude   : longitude,
            Comments    : ""
        },
    };;

    // Send the POST request to the lf_createTask endpoint
    fetch(`/hlf_createTask/${authId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // Assuming you have a getCsrfToken() function to get the CSRF token
        },
        body: JSON.stringify(postData),
    })
    .then((response) => {
        if (response !== 500) {
            console.log('Task Create successfully', response);
            // Redirect to the home page after successful deletion
            window.location.href = '/';
        } else {
            console.error('Error Create Task:', response);
            alert('Failed to Create the Task. Please try again.');
            // Redirect to the home page after showing the failure alert
            window.location.href = '/';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to Create the Task. Please try again.');
        // Redirect to the home page after showing the failure alert
        window.location.href = '/';
    });
};

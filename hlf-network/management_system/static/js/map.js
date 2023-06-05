let map;



function parseCoordinatesUAV(responseData) {
  const coordinates = responseData.map(item => {
      return {
        id: item.pk ,
        name: item.fields.uav_manager
      };
  });
  return coordinates;
}


async function fetchCoordinates() {
  try {
    const response = await fetch('/fanet_getAsset/');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}


async function addMarkersFromData(map) {
  try {
    // 기존 마커 삭제
    if (window.currentMarkers.length > 0) {
      for (let i = 0; i < window.currentMarkers.length; i++) {
        window.currentMarkers[i].remove();
      }
      window.currentMarkers = [];
    }

    const data = await fetchCoordinates();

    // JSON 데이터에서 마커 위치 추출
    const markerData = data.map(item => {
      return {
        position: [parseFloat(item.fields.longitude), parseFloat(item.fields.latitude)],
        title: item.fields.uav_manager
      };
    });

    // 각 위치에 마커 추가
    for (const data of markerData) {
      const iconElement = document.createElement('img');
      iconElement.src = "https://seokhyeon-asset.s3.ap-northeast-2.amazonaws.com/UAV-Managemet-System/uav-icon__black.png";
      const popup = new maplibregl.Popup({
        closeButton: false,
        closeOnClick: false,
        offset: 25
      }).setHTML(`<h3>${data.title}</h3>`);

      const marker = new maplibregl.Marker({ element: iconElement })
        .setLngLat(data.position)
        .setPopup(popup)
        .addTo(map);

      // 마커를 window.currentMarkers 배열에 추가
      window.currentMarkers.push(marker);
    }
  } catch (error) {
    console.error('Error adding markers:', error);
  }
}

function populateDropdown(uavsData) {
  let dropdown = document.getElementById('inputGroupSelect01');
  while (dropdown.firstChild) {
      dropdown.removeChild(dropdown.firstChild);
  }
  for (const uavData of parseCoordinatesUAV(uavsData)) {
      let option = document.createElement('option');
      option.value = uavData.id;
      option.text = uavData.name; // Changed this line to display the name
      dropdown.add(option);
  }
}

document.addEventListener('DOMContentLoaded', async function () {
  const uavData = await fetchCoordinates();
  populateDropdown(uavData);
});

function initMap() {
  const apiKey = "";
  const region = "ap-northeast-1";
  const mapName = "UAV_Management_System";
  const styleUrl = `https://maps.geo.${region}.amazonaws.com/maps/v0/maps/${mapName}/style-descriptor?key=${apiKey}`;
  
  const map = new maplibregl.Map({
    container: "map",
    style: styleUrl,
    center: [116.407395, 39.904211],
    zoom: 11,
  });
  
  map.addControl(new maplibregl.NavigationControl(), "top-left");
  
  const iconElement = document.createElement('img');
  iconElement.src = "https://seokhyeon-asset.s3.ap-northeast-2.amazonaws.com/UAV-Managemet-System/uav-icon__black.png";

    
  map.on('click', function (event) {
    const coordinates = event.lngLat;
    var lat = coordinates.lat;
    var lng = coordinates.lng;
    document.getElementById("latitude-input").value = lat.toFixed(6);
    document.getElementById("longitude-input").value = lng.toFixed(6);
  });
  


  window.currentMarkers = [];
  setInterval(async () => {
    addMarkersFromData(map);
  }, 5000); // 5초마다 좌표 데이터를 가져와서 마커를 업데이트합니다.
}
initMap();

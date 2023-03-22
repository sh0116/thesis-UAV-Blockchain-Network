let map;

function parseCoordinates(responseData) {
  const coordinates = responseData.map(item => {
      return {
          lat: item.fields.latitude,
          lng: item.fields.longitude
      };
  });
  return coordinates;
}

async function fetchCoordinates() {
  try {
    const response = await fetch('/client/');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}


function updateMarkers(map, markersData, icons) {
  // 기존 마커 제거
  for (const marker of window.currentMarkers) {
      marker.setMap(null);
  }
  window.currentMarkers = [];

  // 새로운 마커 생성
  for (const markerData of markersData) {
      const marker = new google.maps.Marker({
          position: markerData,
          map: map,
          icon: icons['uav'].icon,
      });
      window.currentMarkers.push(marker);
  }
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 39.904211, lng: 116.407395 },
    zoom: 8,
  });
  const icons = {
    uav: {
      icon: "https://seokhyeon-asset.s3.ap-northeast-2.amazonaws.com/UAV-Managemet-System/uav-icon.png",
    },
  };

  map.addListener("click", function (event) {
    var lat = event.latLng.lat();
    var lng = event.latLng.lng();

    document.getElementById("latitude-input").value = lat.toFixed(6);
    document.getElementById("longitude-input").value = lng.toFixed(6);

    document.getElementById("clicked-coordinates").innerHTML =
        "Latitude: " + lat.toFixed(6) + ", Longitude: " + lng.toFixed(6);
  });
  window.currentMarkers = [];

  setInterval(async () => {
    const coordinates = await fetchCoordinates();
    updateMarkers(map, coordinates, icons);
  }, 5000); // 5초마다 좌표 데이터를 가져와서 마커를 업데이트합니다.
}
window.initMap = initMap;
//116.407395, 39.904211
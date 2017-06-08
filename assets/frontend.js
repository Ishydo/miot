console.log("Loading homepage JS.")

var GoogleMapsLoader = require('google-maps'); // only for common js environments
GoogleMapsLoader.KEY = 'AIzaSyCWAz__u7xGDOZX7UI_daXZbQqZlPhFC4k';

var myLatLng = {lat: -25.363, lng: 131.044};

GoogleMapsLoader.load(function(google) {
  var map = new google.maps.Map(document.getElementById("map-canvas"), {
    zoom: 4,
    center: myLatLng,
    disableDefaultUI: true,
    fullscreenControl: true,
    zoomControl: true,
    animation: google.maps.Animation.DROP
  });

  var bounds = new google.maps.LatLngBounds();

  var markers = $.parseJSON($("#markers").text())

  $.each(markers, function(index, marker) {

    var info = new google.maps.InfoWindow({
      content: '<a href="' + marker.href + '"><h6 class="poi-name">' + marker.name + '</h6></a>',
      maxWidth: 300
    });

    var pos = new google.maps.LatLng(marker.position.lat, marker.position.lon)
    bounds.extend(pos);

    var marker = new google.maps.Marker({
      position: pos,
      map: map,
    });

    marker.addListener('click', function(){
      info.open(map, marker);
    });
  });

  map.fitBounds(bounds);



  var styledMapType = new google.maps.StyledMapType([
  {
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.neighborhood",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "poi.business",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "transit",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]);

  //Associate the styled map with the MapTypeId and set it to display.
  map.mapTypes.set('styled_map', styledMapType);
  map.setMapTypeId('styled_map');

});

import './frontend.css'

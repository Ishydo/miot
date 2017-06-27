console.log("Loading homepage JS.")

// For map clustering
import "js-marker-clusterer"

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
  });


  // Bounds, in page markers and empty array
  var bounds = new google.maps.LatLngBounds();    // Bounds for auto bounding map
  var markers = $.parseJSON($("#markers").text()) // Markers in DOM (JSON in div)
  var markersArr = [];                            // Marker objects array

  // For each marker in page
  $.each(markers, function(index, marker) {

    // Set position
    var pos = new google.maps.LatLng(marker.position.lat, marker.position.lon)

    // Create the marker on the map
    var gMarker = new google.maps.Marker({position: pos, map: map,});

    // Create the info bubble
    var info = new google.maps.InfoWindow({content: '<a href="'+ marker.href +'"><img src="'+ marker.img +'" style="max-width:100%;" class="rounded"><h6 class="my-1">' + marker.name + '</h6></a>', maxWidth: 300,});

    // Listener on click on marker
    gMarker.addListener('click', function(){info.open(map, gMarker);});

    // Extends bounds and push marker
    bounds.extend(pos);
    markersArr.push(gMarker);

  });


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

  // Auto fit bounds
  map.fitBounds(bounds);

  // Marker clustering
  console.log(markersArr)
  var mcOptions = {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'};
  var mc = new MarkerClusterer(map, markersArr, mcOptions);

});

import './frontend.css'

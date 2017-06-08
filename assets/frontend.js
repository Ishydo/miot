console.log("Loading homepage JS.")

var GoogleMapsLoader = require('google-maps'); // only for common js environments
GoogleMapsLoader.KEY = 'AIzaSyCWAz__u7xGDOZX7UI_daXZbQqZlPhFC4k';

var myLatLng = {lat: -25.363, lng: 131.044};

GoogleMapsLoader.load(function(google) {
    var map = new google.maps.Map(document.getElementById("map-canvas"), {
      zoom: 4,
      center: myLatLng
    });

    var marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      title: 'Hello World!'
    });
});

import './frontend.css'

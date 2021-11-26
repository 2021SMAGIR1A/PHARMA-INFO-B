// // to get current year
// function getYear() {
//     var currentDate = new Date();
//     var currentYear = currentDate.getFullYear();
//     document.querySelector("#displayYear").innerHTML = currentYear;
// }

// getYear();


// // client section owl carousel
// $(".client_owl-carousel").owlCarousel({
//     loop: true,
//     margin: 0,
//     dots: false,
//     nav: true,
//     navText: [],
//     autoplay: true,
//     autoplayHoverPause: true,
//     navText: [
//         '<i class="fa fa-angle-left" aria-hidden="true"></i>',
//         '<i class="fa fa-angle-right" aria-hidden="true"></i>'
//     ],
//     responsive: {
//         0: {
//             items: 1
//         },
//         600: {
//             items: 1
//         },
//         1000: {
//             items: 2
//         }
//     }
// });



// /** google_map js **/
// function myMap() {
//     var mapProp = {
//         center: new google.maps.LatLng(40.712775, -74.005973),
//         zoom: 18,
//     };
//     var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
// }

  
// center, zoom, and maxZoom of the map
var center = [52.45, 13.35],
  zoom = 2,
  moreZoom = 10,
  maxZoom = 18

// get location using the Geolocation interface
var geoLocationOptions = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
}

function success(position) {
  var crd = position.coords,
    latLng = [crd.latitude, crd.longitude]
  // console.log('Your current position is:')
  // console.log(`Latitude : ${crd.latitude}`)
  // console.log(`Longitude: ${crd.longitude}`)
  // console.log(`More or less ${crd.accuracy} meters.`)
  // map.setZoom(moreZoom)
  // map.panTo(latLng)
  // L.marker(latLng).addTo(map)
  //   .bindPopup(`<b>Your location</b><br>
  //                             Latitude: ${crd.latitude} <br>
  //                             Longitude: ${crd.longitude} <br>
  //                             More or less:  ${crd.accuracy} 
  //                             meters`).openPopup();
  var fields={
    "lat":crd.latitude,
    "lng":crd.longitude
  };
  $.ajax({
    url:"/mePos",
    type:'GET',
    data:fields,
    success:function(result){
      console.log(200)
    }
  })
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`)
}

navigator.geolocation.getCurrentPosition(success, error, geoLocationOptions)


// create the map
// var map = L.map('map', {
//   contextmenu: true,
//   contextmenuWidth: 140,
//   contextmenuItems: [{
//       text: 'Center map here',
//       callback: centerMap
//     },
//     {
//       text: 'Add marker here',
//       callback: addMarker
//     }
//   ]
// }).setView(center, zoom)



// set up the OSM layer
// L.tileLayer(
//   'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     maxZoom: maxZoom
//   }).addTo(map)


// // function to center map
// function centerMap(e) {
//   map.panTo(e.latlng)
// }

// // function to add marker
// function addMarker(e) {
//   L.marker(e.latlng).addTo(map)
// }
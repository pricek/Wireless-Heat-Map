/*     var iframe = document.getElementById('googlemaps');
     var coords = [
	{lat: 44.5672185649456, lng: -123.285932120896},
	{lat: 44.5672179182893, lng: -123.286046999104},
	{lat: 44.5669336151982, lng: -123.286049051164},
	{lat: 44.5669322872024, lng: -123.285932124518},
	{lat: 44.5672185649456, lng: -123.285932120896}
     ];
    
     var westGreenhouse = new google.maps.Polygon({
        paths: coords,
	strokeColor: '#FF0000',
	strokeOpacity: 0.8,
	strokeWeight: 2,
	fillColor: '#FF0000',
	fillOpacity: 0.35
     }); 

     westGreenhouse.setMap(iframe);
*/
/*
function polyMap() {
	var iframe = document.getElementById('frameID'),
});

var coords = [
	{lat: -123.285932120896, lng: 44.5672185649456},
	{lat: -123.286046999104, lng: 44.5672179182893},
	{lat: -123.286049051164, lng: 44.5669336151982},
	{lat: -123.285932124518, lng: 44.5669322872024},
	{lat: -123.285932120896, lng: 44.5672185649456},
]

map.data.add({geometry: new google.maps.Data.Polygon([coords])})
*/
var gmap;
	function initMap() {
        	gmap = new google.maps.Map(document.getElementById('gmap'), {
          	center: {lat: 44.564671, lng: -123.279343},
          	zoom: 15
        });
}

function initMap() {
    var center = {lat: 42.35002773853596, lng: -71.10526514445576};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: center
    });
    var marker = new google.maps.Marker;

    map.addListener('click', function(ApiMouseEvent) {

        marker.setMap(null);

        var lat = ApiMouseEvent.latLng.lat();
        var lng = ApiMouseEvent.latLng.lng();
        var locationJson = ApiMouseEvent.latLng.toJSON()

        /*var contentString = '<div id="content" style="text-align:center;">'+lat+','+ lng+'<br/><button onclick="select('+lat+','+lng+');">Select</button></div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });*/
        marker = new google.maps.Marker({
            position: locationJson,
            map: map,
            title: lat+','+lng
        });
        document.getElementById('lat').value = lat
        document.getElementById('lng').value = lng
        //infowindow.open(map, marker);
    });
}

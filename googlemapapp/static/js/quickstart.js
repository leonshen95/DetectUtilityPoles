function initMap() {
    var tiananmen = {lat: 39.90861678016982, lng: 116.39753844220968};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: tiananmen
    });
    var marker = new google.maps.Marker;

    map.addListener('click', function(ApiMouseEvent) {

        marker.setMap(null);

        var lat = ApiMouseEvent.latLng.lat();
        var lng = ApiMouseEvent.latLng.lng();
        var locationJson = ApiMouseEvent.latLng.toJSON()

        var contentString = '<div id="content" style="text-align:center;">'+lat+','+ lng+'<br/><button onclick="select('+lat+','+lng+');">Select</button></div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });
        marker = new google.maps.Marker({
            position: locationJson,
            map: map,
            title: lat+','+lng
        });
        document.getElementById('input').innerHTML = lat+','+lng
        infowindow.open(map, marker);
    });


}

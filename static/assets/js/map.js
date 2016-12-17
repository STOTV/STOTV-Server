    function recovery() {
        var inputs = document.getElementById("recovery").getElementsByTagName("input");
        for (i = 0; i < inputs.length; i++) {
            if (inputs[i].getAttribute("name") == "imei") {
                fetchRecovery(inputs[i].value);
            }
        }
        return false;
    }

    function fetchRecovery(imei) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.status == 200) {
                var json = JSON.parse(xmlhttp.responseText);
                if (json['deviceName'] != undefined) {
                    document.getElementById('recovery').innerHTML = "Congrats you have found " + json['deviceName'] +
                        "!<br /> Please Mail It Back To: <br />" +
                        json['returnName'] + "<br />" + json['returnAddr1'] + "<br />" + json['returnAddr2'] + "<br /><br />Thank you, <br /> The devRant Community Project 2016 Team";

                }
            }
        };
        xmlhttp.open("GET", "/api/v1/found/" + imei, true);
        xmlhttp.send();
    }

    function getLocation(id) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                if (xmlhttp.status == 200) {
                    var json = JSON.parse(xmlhttp.responseText);
                    var mapProp = {
                        zoom: 12,
                        scrollwheel: true,
                        draggable: true,
                        mapTypeId: "hybrid",
                        disableDefaultUI: true,
                        zoomControl: true,
                        zoomControlOptions: {
                            position: google.maps.ControlPosition.LEFT_TOP
                        }
                    };
                    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
                    var bounds = new google.maps.LatLngBounds();
                    var infowindow = new google.maps.InfoWindow();
                    var pathCoords = [];
                    for (var i = 0; i < json.length; i++) {
                        var marker = new google.maps.Marker({
                            position: new google.maps.LatLng(json[i]['latitude'], json[i]['longitude']),
                            map: map
                        });
                        bounds.extend(marker.position);
                        google.maps.event.addListener(marker, 'click', (function (marker, i) {
                            return function () {
                                infowindow.setContent("Name: <a href='?id=" + json[i]['deviceId'] + "'>" + json[i]['name'] + "</a><br>" + "Time: " + json[i]['time'] + "<br>" + "CEP: " + json[i]['cep']);
                                infowindow.open(map, marker);
                            }
                        })(marker, i));
                        pathCoords.push({lat: Number(json[i]['latitude']), lng: Number(json[i]['longitude'])});
                    }


                    var path = new google.maps.Polyline({
                        path: pathCoords,
                        geodesic: true,
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });
                    path.setMap(map);

                    map.fitBounds(bounds);
                    var listener = google.maps.event.addListener(map, "idle", function() {
                        if (map.getZoom() > 5) map.setZoom(5);
                        google.maps.event.removeListener(listener);
                    });
                }
            }
        };
        if (id == undefined) {
            xmlhttp.open("GET", "/api/v1/location", true);
        } else {
            xmlhttp.open("GET", "/api/v1/location/" + id, true);
        }
        xmlhttp.send();
    }

    function getQueryString(name) {
        var query = window.location.search.substring(1);
        var vars = query.split('&');
        for (i = 0; i < vars.length; i++) {
            var split = vars[i].split('=');
            if (decodeURIComponent(split[0]) == name) {
                return decodeURIComponent(split[1])
            }
        }
        return undefined;
    }

    google.maps.event.addDomListener(window, 'load', function () {
        var found = getQueryString("imei");
        if (found != undefined) {
            fetchRecovery(found);
        }
        getLocation(getQueryString("id"));
    });

class Map(object):
    def __init__(self):
        self._points = []
        self._positions = []
        self._player = None
    def add_point(self, coordinates, color="#FF0000"):
        self._points.append((coordinates, color))
    def add_position(self, coordinates):
        self._positions.append(coordinates)
    def __str__(self):
        centerLat = sum((x[0] for x in self._positions)) / len(self._positions)
        centerLon = sum((x[1] for x in self._positions)) / len(self._positions)
        pathCode = """
            var walkPathCoords = [{path}];
            var walkPath = new google.maps.Polyline({{
                path: walkPathCoords,
                geodesic: true,
                strokeColor: '#7F00FF',
                strokeOpacity: 0.5,
                strokeWeight: 4}});
            walkPath.setMap(map);
        """.format(path=",".join(["new google.maps.LatLng(%f,%f)" % (p[0], p[1]) for p in self._positions]))
        markersCode = "\n".join(
            ["""var marker = new google.maps.Marker({{
                position: {{lat: {lat}, lng: {lng}}},
                map: map
                }});
                marker.setIcon('{icon}');""".format(lat=x[0][0], lng=x[0][1], icon=x[1]) for x in self._points
            ])
        playerCode = """var marker = new google.maps.Marker({{
                        position: {{lat: {lat}, lng: {lng}}},
                        map: map
                        }});
                        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/purple.png');""".format(lat=self._player[0], lng=self._player[1])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 16,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {pathCode}
                    {markersCode}
                    {playerCode}
                    var bounds = new google.maps.LatLngBounds();
                    var arrayLength = walkPathCoords.length;
                    for (var i = 0; i < arrayLength; i++) {{
                        bounds.extend(walkPathCoords[i]);
                    }}
                    map.fitBounds(bounds);
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   pathCode=pathCode, playerCode=playerCode,
                   markersCode=markersCode)

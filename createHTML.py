import googlemaps
import os.path
import os
import webbrowser

def get_route_from_ranking(tour, places):
	"""
	Matches the rankings from the tour generated via MST/DFS
	with the destinations.
	"""
	optimal_route = [places[stop] for stop in tour]

	return optimal_route


def create_optimal_route_html(optimal_route, distance, display=True):
	output_file = 'output_route.html'
	optimal_route = list(optimal_route)
	optimal_route += [optimal_route[0]]

	Page_1 = """
	<!DOCTYPE html>
	<html lang="en">
	  <head>
		<meta charset="utf-8">
		<meta name="viewport" content="initial-scale=1.0, user-scalable=no">
		<meta name="description" content="Display a 2-approximate tour given set of destinations.">
		<meta name="author" content="Melody Lin">
		
		<title>A kinda optimal tour through required points of interest.</title>
		<style>
		  	html, body, #map-canvas {
				height: 100%;
				margin: 0px;
				padding: 0px
			}
			#panel {
				position: absolute;
				top: 5px;
				left: 50%;
				margin-left: -180px;
				z-index: 5;
				background-color: #fff;
				padding: 10px;
				border: 1px solid #999;
			}
		</style>
		<script>
		</script>
		<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCGUqXGZbLcBljoPSj8iA011drrMo999AQ"></script>
		<script>
			var routes_list = []
			var markerOptions = {icon: "http://maps.gstatic.com/mapfiles/markers2/marker.png"};
			var directionsDisplayOptions = {preserveViewport: true,
											markerOptions: markerOptions};
			var directionsService = new google.maps.DirectionsService();
			var map;

			function initialize() {
				var center = new google.maps.LatLng(34.0505677, -118.2492406);
				var mapOptions = {
					zoom: 15,
					center: center
				};

				map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
				for (i = 0; i < routes_list.length; i++){
					routes_list[i].setMap(map)
				}
			}

			function calculateAndDisplayRoute(directionsService, start, end, routes) {
			  
				var directionsDisplay = new google.maps.DirectionsRenderer(directionsDisplayOptions);

				var waypoints = [];
				for (var i = 0; i < routes.length; i++) {
				waypoints.push({
					location: routes[i],
					stopover: true});
				}
			  
				var request = {
					origin: start,
					destination: end,
					waypoints: waypoints,
					optimizeWaypoints: false,
					travelMode: 'DRIVING'
				};

				directionsService.route(request, function(response, status) {
					if (status == google.maps.DirectionsStatus.OK) {
						directionsDisplay.setDirections(response);
					}
			  	});

				routes_list.push(directionsDisplay);
			}

			function createRoutes(route) {
				
				midPoints = route.slice(1, (route.length - 1));
				calculateAndDisplayRoute(directionsService, route[0], route[route.length - 1], midPoints);
			}
	"""
	Page_2 = """
			createRoutes(optimal_route);
			google.maps.event.addDomListener(window, 'load', initialize);

		</script>
		</head>
		<body>
			<div id="map-canvas"></div>
		</body>
	</html>
	"""

	localoutput_file = output_file

	with open(localoutput_file, 'w') as fs:
		fs.write(Page_1)
		fs.write("\t\t\toptimal_route = {0}".format(str(optimal_route)))
		fs.write(Page_2)

	if display:
		webbrowser.open_new_tab(localoutput_file)
import re
from TSPResult import TSPResult as tsp
from DMRequest import DMRequest as dmr

def get_tour(num_points, msg, places):
	num_points2 = num_points
	start_str = '%d %d' % (num_points, num_points2)

	# Search the Concorde log for the start of city numbers
	# Get the index where the numbers are first listed
	start = msg.find(start_str)
	legs = msg[( start + len(start_str + 1) ):]
	indices = re.findall(r'(\d+) \d+ \d+', legs)
	tour = map(lambda x: places['destinations'][int(x)], indices)
	tour.append(tour[0])

	print(tour)
	return tour

def create_routes(tour):
	routes = []
	length = len(tour)
	i = 1

	while length >= 2:
		rlength = min( 8, length - 2 )
		start = tour[0]
		end = tour[rlength + 1]
		route = tour[ 1 : rlength + 1 ]
		routes.append( (i, start, end, route) )
		i += 1
		tour = tour[rlength + 1:]
		length = len(tour)

	print(routes)
	return routes

if __name__ == "__main__":
	# List of places to include on the tour
	places = {
		'origins': ["Arcadia, CA 91007", "Movie Flat Rd, Lone Pine, CA 93545", "Manzanar Reward Rd, California", "Devils Postpile Access Road, Mammoth Lakes, CA 93546", "Mono Lake, CA"],
		'destinations': ["Arcadia, CA 91007", "Movie Flat Rd, Lone Pine, CA 93545", "Manzanar Reward Rd, California", "Devils Postpile Access Road, Mammoth Lakes, CA 93546", "Mono Lake, CA"]
	}
	
	# Create a Distance Matrix Request object
	# --> get_matrix() will make a GET request to the Google DM API 
	# --> get_response_data() will store the response values into a dictionary
	# --> build_lower_triangle_matrix() generates a matrix in TSPLib format for NEOS
	# distances_lt variable will be used for NEOS computation of an optimal tour
	#dm = dmr(places)
	#dm.data = dm.get_response_data(dm.get_matrix())
	#distances_lt = dm.build_lower_triangle_matrix(dm.data)

	# temp data so we do not have to keep making requests to Google's API
	distances_lt = [[     0,      0,      0,      0,      0],
					[357938,      0,      0,      0,      0],
					[366042,  23361,      0,      0,      0],
					[531201, 188520, 165286,      0,      0],
					[547170, 204489, 181254,  60864,      0]]
	# Create a TSP Result object to handle requests to NEOS server
	# --> Build an XML using the distances_lt data
	# --> Submit a job to the NEOS server
	# --> Parse result log for tour
	tsp_xml = tsp.get_xml_with_data( len(places['origins']), distances_lt )
	result = tsp().run_tsp_job(tsp_xml)
	tour = get_tour( len(places['destinations']), solution, places )
	routes = create_routes(tour)
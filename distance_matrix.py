from TSPResult import TSPResult as tsp
from DMRequest import DMRequest as dmr
from Graph import Graph
from Vertex import Vertex
from PrimMST import primMST, printMST

if __name__ == "__main__":
	# List of places to include on the tour
	places = {
		'origins': ["Arcadia, CA 91007", "Movie Flat Rd, Lone Pine, CA 93545", "Manzanar Reward Rd, California", "Devils Postpile Access Road, Mammoth Lakes, CA 93546", "Mono Lake, CA"],
		'destinations': ["Arcadia, CA 91007", "Movie Flat Rd, Lone Pine, CA 93545", "Manzanar Reward Rd, California", "Devils Postpile Access Road, Mammoth Lakes, CA 93546", "Mono Lake, CA"]
	}
	
	######################################################################################################
	## Create a Distance Matrix Request object															##
	## --> get_distances() will make a GET request to the Google DM API									##
	## --> get_response_data() will store the response values into a dictionary							##
	######################################################################################################
	
	# dm = dmr(places)
	# dm.data = dm.get_response_data(dm.get_distances())

	distances = [[0, 358158, 366153, 531506, 547295], 
				 [357938, 0, 23252, 188605, 204393], 
				 [366042, 23361, 0, 165558, 181347], 
				 [531201, 188520, 165271, 0, 60864], 
				 [547170, 204489, 181240, 60864, 0]]

	g = Graph(5, distances)
	mst = primMST(g)
	printMST(mst, g, places['origins'])

	# saving upper and lower matrix configurations in case we need it later
	# so we don't have to keep making requests to Google's API
	# distances_ut = [[     0, 358158, 366153, 531506, 547295],
	#  				[     0,      0,  23252, 188605, 204393],
	#  				[     0,      0,      0, 165558, 181347],
	#  				[     0,      0,      0,      0,  60864],
	#  				[     0,      0,      0,      0,      0]]

	# distances_lt = [[     0,      0,      0,      0,      0],
	# 				[357938,      0,      0,      0,      0],
	# 				[366042,  23361,      0,      0,      0],
	# 				[531201, 188520, 165286,      0,      0],
	# 				[547170, 204489, 181254,  60864,      0]]
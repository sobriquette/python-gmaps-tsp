from TSPResult import TSPResult as tsp
from DMRequest import DMRequest as dmr
from Graph import Graph
from Vertex import Vertex
from PrimMST import prim_mst, print_mst, dfs_mst

if __name__ == "__main__":
	# List of places to include on the tour
	places = {
		'origins': ["317 S Broadway, Los Angeles, CA 90013", "845 Alameda St, Los Angeles, CA 90012", "221 S Grand Ave, Los Angeles, CA 90012", "111 S Grand Ave, Los Angeles, CA 90012"],
		'destinations': ["317 S Broadway, Los Angeles, CA 90013", "845 Alameda St, Los Angeles, CA 90012", "221 S Grand Ave, Los Angeles, CA 90012", "111 S Grand Ave, Los Angeles, CA 90012"]
	}
	
	######################################################################################################
	## Create a Distance Matrix Request object															##
	## --> get_distances() will make a GET request to the Google DM API									##
	## --> get_response_data() will store the response values into a dictionary							##
	######################################################################################################
	
	# dm = dmr(places)
	# dm.data = dm.get_response_data(dm.get_distances())
	# print(dm.data)

	# distances1 = [[0, 358158, 366153, 531506, 547295], 
	# 			 [357938, 0, 23252, 188605, 204393], 
	# 			 [366042, 23361, 0, 165558, 181347], 
	# 			 [531201, 188520, 165271, 0, 60864], 
	# 			 [547170, 204489, 181240, 60864, 0]]

	distances = [[0, 1553, 685, 704], 
				 [1568, 0, 1728, 1594], 
				 [685, 1713, 0, 609], 
				 [901, 1596, 808, 0]]

	g = Graph(len(distances), distances)
	mst = prim_mst(g)
	
	# we have a minimum spanning tree!
	print_mst(mst, g, places['origins'])

	tour = dfs_mst(mst)
	# this is the order we should travel in
	print(tour)

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
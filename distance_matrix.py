from TSP import Graph, Vertex, PrimMST
from TSP.ConcordeResult import ConcordeResult
from TSP.DMRequest import DMRequest
from createHTML import create_optimal_route_html, get_route_from_ranking
from GA import *
from itertools import combinations

if __name__ == "__main__":
	# List of places to include on the tour
	places = [
		"Arcadia, CA 91007, USA",
        "Movie Flat Rd, Lone Pine, CA 93545, USA",
        "1 Ahwahnee Drive, YOSEMITE NATIONAL PARK, CA 95389",
        "Mono Lake, California 93541, USA",
        "1600 Amphitheatre Pkwy, Mountain View, CA 94043",
        "450 Powell St, San Francisco, CA 94102"
	]
	
	# Parameters for genetic algorithm
	generations = 5000
	population_size = 100

	######################################################################################################
	## Create a Distance Matrix Request object															##
	## --> get_distances() will make a GET request to the Google DM API									##
	## --> get_response_data() will store the response values into a dictionary							##
	######################################################################################################
	
	# dm = DMRequest()
	# waypoints_data = dm.get_response_data(places)
	# print(waypoints_data['waypoints_distances'])

	# DTLA POI
	# waypoints_distances = {
	# 	frozenset({'317 S Broadway, Los Angeles, CA 90013', '845 Alameda St, Los Angeles, CA 90012'}): 1553, 
	# 	frozenset({'221 S Grand Ave, Los Angeles, CA 90012', '317 S Broadway, Los Angeles, CA 90013'}): 685, 
	# 	frozenset({'317 S Broadway, Los Angeles, CA 90013', '111 S Grand Ave, Los Angeles, CA 90012'}): 704, 
	# 	frozenset({'221 S Grand Ave, Los Angeles, CA 90012', '845 Alameda St, Los Angeles, CA 90012'}): 1728, 
	# 	frozenset({'111 S Grand Ave, Los Angeles, CA 90012', '845 Alameda St, Los Angeles, CA 90012'}): 1594, 
	# 	frozenset({'221 S Grand Ave, Los Angeles, CA 90012', '111 S Grand Ave, Los Angeles, CA 90012'}): 609
	# }

	# Cali POI
	waypoints_distances = {
		frozenset({'Movie Flat Rd, Lone Pine, CA 93545, USA', 'Arcadia, CA 91007, USA'}): 358158, 
		frozenset({'1 Ahwahnee Drive, YOSEMITE NATIONAL PARK, CA 95389', 'Arcadia, CA 91007, USA'}): 545197, 
		frozenset({'Mono Lake, California 93541, USA', 'Arcadia, CA 91007, USA'}): 547295, 
		frozenset({'1600 Amphitheatre Pkwy, Mountain View, CA 94043', 'Arcadia, CA 91007, USA'}): 581398, 
		frozenset({'450 Powell St, San Francisco, CA 94102', 'Arcadia, CA 91007, USA'}): 626395, 
		frozenset({'1 Ahwahnee Drive, YOSEMITE NATIONAL PARK, CA 95389', 'Movie Flat Rd, Lone Pine, CA 93545, USA'}): 324301, 
		frozenset({'Mono Lake, California 93541, USA', 'Movie Flat Rd, Lone Pine, CA 93545, USA'}): 204393, 
		frozenset({'1600 Amphitheatre Pkwy, Mountain View, CA 94043', 'Movie Flat Rd, Lone Pine, CA 93545, USA'}): 687452, 
		frozenset({'450 Powell St, San Francisco, CA 94102', 'Movie Flat Rd, Lone Pine, CA 93545, USA'}): 575846, 
		frozenset({'1 Ahwahnee Drive, YOSEMITE NATIONAL PARK, CA 95389', 'Mono Lake, California 93541, USA'}): 125678, 
		frozenset({'1 Ahwahnee Drive, YOSEMITE NATIONAL PARK, CA 95389', '1600 Amphitheatre Pkwy, Mountain View, CA 94043'}): 338190, 
		frozenset({'1 Ahwahnee Drive, YOSEMITE NATIONAL PARK, CA 95389', '450 Powell St, San Francisco, CA 94102'}): 338288, 
		frozenset({'1600 Amphitheatre Pkwy, Mountain View, CA 94043', 'Mono Lake, California 93541, USA'}): 401124, 
		frozenset({'450 Powell St, San Francisco, CA 94102', 'Mono Lake, California 93541, USA'}): 401222, 
		frozenset({'450 Powell St, San Francisco, CA 94102', '1600 Amphitheatre Pkwy, Mountain View, CA 94043'}): 58197
	}

	# distances1 = [[0, 358158, 366153, 531506, 547295], 
	# 			 [357938, 0, 23252, 188605, 204393], 
	# 			 [366042, 23361, 0, 165558, 181347], 
	# 			 [531201, 188520, 165271, 0, 60864], 
	# 			 [547170, 204489, 181240, 60864, 0]]
	
	# distances2 = [[0, 1553, 685, 704], 
	# 			 [1568, 0, 1728, 1594], 
	# 			 [685, 1713, 0, 609], 
	# 			 [901, 1596, 808, 0]]

	distances = [
		[0, 358158, 324301, 204393, 687452, 575846],
		[358158, 0, 545197, 547295, 581398, 626395],
		[324301, 545197, 0, 125678, 338190, 338288],
		[204393, 547295, 125678, 0, 401124, 401222],
		[687452, 581398, 338190, 401124, 0, 58197],
		[575846, 626395, 338288, 401222, 58197, 0]
	]

	##############################################################################
	## Solution 1: use the NEOS CONCORDE solver to calculate a tour				##
	## Result: Concorde won't accept the XML :'(								##
	##############################################################################
	## neos_client = ConcordeResult()
	## result = neos_client.solve_tsp_with_neos_concorde(dist_full_matrix)

	##############################################################################
	## Solution 2: a 2-opt approximation of the traveling salesman problem.		##
	## We construct a graph using the distances as weights.						##
	## Then we construct a minimum spanning tree.								##
	## Finally, we do a preorder walk of the MST to get the tour.				##
	##############################################################################
	g = Graph.Graph(len(distances), distances)
	mst = PrimMST.prim_mst(g)
	tour = PrimMST.dfs_mst(mst)
	optimal_route = get_route_from_ranking(tour, places)
	create_optimal_route_html(optimal_route, 1, "results-MST", True)
	
	##############################################################################
	## Solution 3: apply a genetic algorithm written by Randy S. Olson			##
	## Source to original GitHub code provided in README						##
	##############################################################################
	optimal_route = run_genetic_algorithm(places, waypoints_distances, generations, population_size)
	create_optimal_route_html(optimal_route, 1, "results-GA", True)

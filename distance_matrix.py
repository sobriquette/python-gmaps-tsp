from TSP import Graph, Vertex, PrimMST
from TSP.ConcordeResult import ConcordeResult
from TSP.DMRequest import DMRequest
from TSP.GA import *
from createHTML import create_optimal_route_html, get_route_from_ranking
from itertools import combinations

def build_full_distance_matrix(waypoints_distances, num_waypoints):
	distances = [[0] * num_waypoints] * num_waypoints
	print(distances)

if __name__ == "__main__":
	# List of places to include on the tour
	places = [
		"805 W Camino Real Ave, Arcadia, CA 91007, USA",
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
	## --> get_response_data() will make a request to Google and store response in a dictionary			##
	######################################################################################################
	dm = DMRequest(places)

	##############################################################################
	## Solution 1: use the NEOS CONCORDE solver to calculate a tour				##
	## Result: Concorde won't accept the XML :'(								##
	##############################################################################
	# neos_client = ConcordeResult()
	# result = neos_client.solve_tsp_with_neos_concorde(dist_full_matrix)

	##############################################################################
	## Solution 2: a 2-opt approximation of the traveling salesman problem.		##
	## We construct a graph using the distances as weights.						##
	## Then we construct a minimum spanning tree.								##
	## Finally, we do a preorder walk of the MST to get the tour.				##
	##############################################################################
	waypoints_data_mst = dm.get_response_data_mst()

	if waypoints_data_mst:
		# Use only data from upper triangle matrix because
		# TSP requires that distance between A <--> B must be same
		# in both directions
		# BUT Google Maps returns different values for A -> B and B -> A
		upper_tri_matrix = DMRequest.build_upper_triangle_matrix(waypoints_data_mst)
		full_matrix = DMRequest.build_full_distance_matrix(upper_tri_matrix)

		# We build a graph and minimum spanning tree from the distances
		# then perform a preorder walk to get the recommended route
		g = Graph.Graph(len(full_matrix), full_matrix)
		mst = PrimMST.prim_mst(g)
		tour = PrimMST.dfs_mst(mst)
		optimal_route = get_route_from_ranking(tour, places)

		create_optimal_route_html(optimal_route, 1, "results-MST", True)
	else:
		raise Exception("Request did not return data for MST version")

	##########################################################################
	## Solution 3: apply a genetic algorithm written by Randy S. Olson		##
	## Source to original GitHub code provided in README					##
	##########################################################################
	waypoints_data_ga = dm.get_response_data_ga()

	if waypoints_data_ga:
		waypoints_distances = waypoints_data_ga['waypoints_distances']

		optimal_route = run_genetic_algorithm(places, waypoints_distances, generations, population_size)
		create_optimal_route_html(optimal_route, 1, "results-GA", True)
	else:
		raise Exception("Request did not return data for GA version")
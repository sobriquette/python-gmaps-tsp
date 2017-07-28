from TSPResult import TSPResult as tsp
from DMRequest import DMRequest as dmr
from Graph import Graph
from Vertex import Vertex
from ShortestPath import dijkstra, shortest

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

	# Build a graph from API response
	g = Graph()

	for i in range(len(places['origins'])):
		g.add_vertex(i)

	for i in range(len(distances_lt)):
		for j in range(i):
			g.add_edge(i, j, distances_lt[i][j])

	# Check that graph is built correctly
	print("Graph data: ")
	for v in g:
		for w in v.get_connections():
			vid = v.get_id()
			wid = w.get_id()
			print('(%s, %s, %3d)' % (vid, wid, v.get_weight(w)))

	# Get shortest paths from node to node
	dijkstra(g, g.get_vertex(0))

	for t in range(len(places['origins'])):
		target = g.get_vertex(t)
		path = [t]
		shortest(target, path)
		print("The shortest path for {} : {}".format(t, path[::-1]))

	############################################################################
	############################################################################
	# Create a TSP Result object to handle requests to NEOS server
	# --> Build an XML using the distances_lt data
	# --> Submit a job to the NEOS server
	# --> Parse result log for tour
	# tsp_xml = tsp.get_xml_with_data( len(places['origins']), distances_lt )
	# result = tsp().run_tsp_job(tsp_xml)
	# tour = get_tour( len(places['destinations']), solution, places )
	# routes = create_routes(tour)
	############################################################################
	############################################################################
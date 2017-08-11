from Vertex import Vertex
from Graph import Graph

def print_mst(parent, graph, places):
	"""
	Prints the constructed MST along with labels of our destinations
	"""
	num_vertices = graph.num_vertices
	adj_matrix = graph.adjacency_matrix
	print("Edge \tWeight \tPlace")
	for i in range(1, num_vertices):
		print( parent[i], "-", i, "\t", adj_matrix[i][parent[i]], " ", \
			   places[i - 1], "to ", places[i] )

def find_min_key(keys, mstSet, num_vertices):
	"""
	Finds vertex with minimum distance value 
	given the set of vertices not included in the MST
	"""

	# Initialize min value
	min_key = float('inf')

	for vertex in range(num_vertices):
		if keys[vertex] < min_key and vertex not in mstSet:
			min_key = keys[vertex]
			min_index = vertex

	return min_index

def prim_mst(graph):
	"""
	Builds a minimum spanning tree using Prim's Algorithm using
	a graph represented as an adjacency matrix.

	Time complexity: O(V^2)
	Space: O(V^2)
	"""

	num_vertices = graph.num_vertices
	adj_matrix = graph.adjacency_matrix

	keys = [float('inf')] * num_vertices 	# Stored key values to pick minimum weight edge in cut
	parent = [None] * num_vertices 			# This will store the constructed MST
	keys[0] = 0								# This will be picked as the first vertex
	mstSet = set()

	parent[0] = -1							# First node is root

	for cout in range(num_vertices):
		# Pick the minimum distance vertex from vertices not yet processed
		curr_source = find_min_key(keys, mstSet, num_vertices)
		# Put the minimum distance vertex in the MST
		mstSet.add(curr_source)
		# Update distance value of adjacent vertices of chosen vertex...
		# only if the new distance is less than the current distance,
		# and teh vertex is not already in the MST
		for neighbor in range(num_vertices):
			# adj_matrix[curr_source][neighbor] is non-zero only for adjacent vertices of m
			# mstSet[neighbor] is False for vertices not yet in the MST
			# Update the key only if adj_matrix[curr_source][neighbor] is smaller than keys[neighbor]
			if adj_matrix[curr_source][neighbor] > 0 and neighbor not in mstSet and \
				keys[neighbor] > adj_matrix[curr_source][neighbor]:
					keys[neighbor] = adj_matrix[curr_source][neighbor]
					parent[neighbor] = curr_source

	return parent

def dfs_mst(mst):
	"""
	Performs depth-first traversal on the minimum spanning tree.
	But since the MST is represented as a list, we turn it back into a graph first.
	"""
	g = Graph()
	for i in range(1, len(mst)):
		g.add_edge(mst[i], i)

	neighbors = [g.vertex_dict[0]]		# stack that holds all adjacent nodes of a vertex
	print(neighbors)
	visited = set()						# tracks which vertices we've seen
	visited.add(0)						# start with source vertex

	result = [0]

	while len(neighbors) > 0:
		adjacent_vertices_for_v = neighbors.pop()
		for v in adjacent_vertices_for_v:
			if v not in visited:
				neighbors.append(g.vertex_dict[v])
				visited.add(v)
				result.append(v)

	return result

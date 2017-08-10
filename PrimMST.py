"""
Sources:																			
http://www.bogotobogo.com/python/python_Prims_Spanning_Tree_Data_Structure.php
http://interactivepython.org/runestone/static/pythonds/Graphs/PrimsSpanningTreeAlgorithm.html
"""

from Vertex import Vertex
from Graph import Graph

##################################################
##		 Prim's MST for Adjacency Matrix		##
## 		 Runtime: 	O(V^2)						##
## 		 Space: 	O(V^2)						##
##################################################

# Utility function to print constructed MST from primMST()
def printMST(parent, graph, places):
	num_vertices = graph.num_vertices
	adj_matrix = graph.adjacency_matrix
	print("Edge \tWeight \tPlace")
	for i in range(1, num_vertices):
		print( parent[i], "-", i, "\t", adj_matrix[i][parent[i]], " ", places[i - 1], "to ", places[i][:7] )

# Utility function to find vertex with minimum distance value,
# given the set of vertices not included in the MST
def minKey(keys, mstSet, num_vertices):
	# Initialize min value
	min_key = float('inf')

	for vertex in range(num_vertices):
		if keys[vertex] < min_key and mstSet[vertex] == False:
			min_key = keys[vertex]
			min_index = vertex

	return min_index

# Prim's Algorithm from GeeksforGeeks
def primMST(graph):
	num_vertices = graph.num_vertices
	adj_matrix = graph.adjacency_matrix

	keys = [float('inf')] * num_vertices 	# Stored key values to pick minimum weight edge in cut
	parent = [None] * num_vertices 			# This will store the constructed MST
	keys[0] = 0								# This will be picked as the first vertex
	mstSet = [False] * num_vertices

	parent[0] = -1							# First node is root

	for cout in range(num_vertices):
		# Pick the minimum distance vertex from vertices not yet processed
		curr_source = minKey(keys, mstSet, num_vertices)
		# Put the minimum distance vertex in the MST
		mstSet[curr_source] = True
		# Update distance value of adjacent vertices of chosen vertex...
		# only if the new distance is less than the current distance,
		# and teh vertex is not already in the MST
		for neighbor in range(num_vertices):
			# adj_matrix[curr_source][neighbor] is non-zero only for adjacent vertices of m
			# mstSet[neighbor] is False for vertices not yet in the MST
			# Update the key only if adj_matrix[curr_source][neighbor] is smaller than keys[neighbor]
			if adj_matrix[curr_source][neighbor] > 0 and mstSet[neighbor] is False and \
				keys[neighbor] > adj_matrix[curr_source][neighbor]:
					keys[neighbor] = adj_matrix[curr_source][neighbor]
					parent[neighbor] = curr_source

	return parent
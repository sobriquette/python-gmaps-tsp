######################################################################################
## Source:																			##
## http://www.bogotobogo.com/python/python_Prims_Spanning_Tree_Data_Structure.php	##
######################################################################################

from Vertex import Vertex
from Graph import Graph
import heapq

def shortest(v, path):
	# build a shortest path from v.previous
	if v.previous:
		path.append(v.previous.get_id())
		shortest(v.previous, path)
	return

def dijkstra(graph, start):
	# set distance for start
	start.set_distance(0)

	# put pair into priority queue
	unvisited_queue = [(v.get_distance(), v) for v in graph]
	heapq.heapify(unvisited_queue)

	while len(unvisited_queue):
		# pop vertex with smallest distance
		uv = heapq.heappop(unvisited_queue)
		current = uv[1]
		current.set_visited()

		for next in current.adjacent:
			if next.visited:
				continue
			new_dist = current.get_distance() + current.get_weight(next)

			if new_dist < next.get_distance():
				next.set_distance(new_dist)
				next.set_previous(current)
				print("updated: current = {}, next = {}, new_dist = {}".format(current.get_id(), next.get_id(), next.get_distance()))
			else:
				print("not updated: current = {}, next = {}, new_dist = {}".format(current.get_id(), next.get_id(), next.get_distance()))

		# Rebuild heap
		# pop every item
		while len(unvisited_queue):
			heapq.heappop(unvisited_queue)
		# put all unvisited vertices into queue
		unvisited_queue = [(v.get_distance(), v) for v in graph if not v.visited]
		heapq.heapify(unvisited_queue)
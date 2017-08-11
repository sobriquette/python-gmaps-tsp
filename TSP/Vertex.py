######################################################################################
## Source:																			##
## http://www.bogotobogo.com/python/python_Prims_Spanning_Tree_Data_Structure.php	##
######################################################################################
from functools import total_ordering

@total_ordering
class Vertex(object):
	def __init__(self, node):
		self.id = node
		self.adjacent = {}

		# Set distance to infinity for all nodes
		self.distance = float('inf')
		# Mark all nodes unvisited
		self.visited = False
		# Predecessor
		self.previous = None

	def add_neighbor(self, neighbor, weight=0):
		self.adjacent[neighbor] = weight

	def get_connections(self):
		return self.adjacent.keys()

	def get_id(self):
		return self.id

	def get_weight(self, neighbor):
		return self.adjacent[neighbor]

	def get_distance(self):
		return self.distance

	def set_distance(self, dist):
		self.distance = dist

	def set_previous(self, prev):
		self.previous = prev

	def set_visited(self):
		self.visited = True

	def __str__(self):
		return str(self.id) + ' next to: ' + str([x.id for x in self.adjacent])

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.distance == other.distance
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, self.__class__):
			return self.distance < other.distance
		return NotImplemented

	def __hash__(self):
		return id(self)
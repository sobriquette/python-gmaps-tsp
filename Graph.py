######################################################################################
## Source:																			##
## http://www.bogotobogo.com/python/python_Prims_Spanning_Tree_Data_Structure.php	##
######################################################################################
from Vertex import Vertex

class Graph(object):
	def __init__(self):
		self.vertex_dict = {}
		self.num_vertices = 0

	def __iter__(self):
		return iter(self.vertex_dict.values())

	def __contains__(self, n):
		return n in self.vertex_dict

	def set_previous(self, current):
		self.set_previous = current

	def get_vertex(self, n):
		if n in self.vertex_dict:
			return self.vertex_dict[n]
		else:
			 return None

	def get_vertices(self):
		return self.vertex_dict.keys()

	def get_previous(self, current):
		return self.get_previous

	def add_vertex(self, node):
		self.num_vertices = self.num_vertices + 1
		new_vertex = Vertex(node)
		self.vertex_dict[node] = new_vertex
		return new_vertex

	def add_edge(self, f, t, cost=0):
		if f not in self.vertex_dict:
			new_vertex = self.add_vertex(f)
		if t not in self.vertex_dict:
			new_vertex = self.add_vertex(t)
		self.vertex_dict[f].add_neighbor(self.vertex_dict[t], cost)
		self.vertex_dict[t].add_neighbor(self.vertex_dict[f], cost)


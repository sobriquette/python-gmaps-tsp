import TSP.Vertex

class Graph(object):
	def __init__(self, num_vertices=0, data=None):
		self.adjacency_matrix = data 		# format needed for building a mst using prim's
		self.vertex_dict = {} 				# holds each vertex and its neighbors
		self.num_vertices = num_vertices

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

	def add_edge_between_vertices(self, f, t, cost=0):
		"""
		Adds edge between two given vertices to the vertex_dict.
		Creates a new Vertex object for each given vertex, and assigns it a weight.

		This was being used in the BogoToBogo tutorial for Prim...
		...but we're not using it currently.
		"""
		if f not in self.vertex_dict:
			new_vertex = self.add_vertex(f)
		if t not in self.vertex_dict:
			new_vertex = self.add_vertex(t)
		self.vertex_dict[f].add_neighbor(self.vertex_dict[t], cost)
		self.vertex_dict[t].add_neighbor(self.vertex_dict[f], cost)

	def add_edge(self, v1, v2):
		"""
		Adds an edge between the two given vertices to vertex_dict
		"""
		if v1 not in self.vertex_dict:
			self.vertex_dict[v1] = []
		if v2 not in self.vertex_dict:
			self.vertex_dict[v2] = []
		self.vertex_dict[v1].append(v2)
		self.vertex_dict[v2].append(v1)
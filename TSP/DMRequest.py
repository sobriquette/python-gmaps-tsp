import requests, os
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from itertools import combinations

class DMRequest(object):
	def __init__(self, places):
		self.base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
		self.api_key = os.environ['DistanceMatrix_APIKEY']
		self.places = places
	
	def __get_distances(self, params):
		"""
		Sends GET request to the Google Distance Matrix API
		"""
		return requests.get(self.base_url, params=params).json()

	def get_response_data_mst(self):
		response = self.__get_distances(self.set_params())

		data = {'distance': [], 'duration': []}
		
		for r in response['rows']:
			distances = []
			durations = []
			for e in r['elements']:
				distances.append(e['distance']['value'])
				durations.append(e['duration']['value'])
			data['distance'].append(distances)
			data['duration'].append(durations)
		
		return data

	def get_response_data_ga(self):
		"""
			Send GET request to Google Distance Matrix API
			Using a format for the genetic algorithm
			Parse API response for distance and duration values
		"""
		data = {'waypoints_distances': {}, 'waypoints_durations': {}}

		for (waypoint1, waypoint2) in combinations(self.places, 2):
			try:
				config = {
					'origins': waypoint1,
					'destinations': waypoint2,
					'key': self.api_key
				}

				response = self.__get_distances(self.set_params(config))

				distance = response['rows'][0]['elements'][0]['distance']['value']
				duration = response['rows'][0]['elements'][0]['duration']['value']

				data['waypoints_distances'][frozenset([waypoint1, waypoint2])] = distance
				data['waypoints_durations'][frozenset([waypoint1, waypoint2])] = duration
			
			except Exception as e:
				print("Could not find route from %s to %s." % (waypoint1, waypoint2))

		return data

	def set_params(self, custom_params=None):
		if custom_params:
			my_params = custom_params
		else:
			my_params = {
					'origins': '|'.join(self.places),
					'destinations': '|'.join(self.places),
					'key': self.api_key,
				}
			
		return my_params

	@staticmethod
	def print_distance_matrix_table(data, places):
		"""
		Creates a distance matrix for TSP computation by the Concorde Solver.
		This will be used when we submit a job to the NEOS server.
		"""
		distances = data['distance']

		df = pd.DataFrame(distances, columns=places, index=places)
		dm = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
		return dm

	@staticmethod
	def build_full_distance_matrix(upper_triangle):
		out = upper_triangle.T + upper_triangle
		np.fill_diagonal(out, np.diag(upper_triangle))
		return out

	@staticmethod
	def build_lower_triangle_matrix(data):
		"""
		Lower triangle matrix format in case we need to use for solving TSP
		"""
		lt = np.tril(data['distance'])
		return lt

	@staticmethod
	def build_upper_triangle_matrix(data):
		"""
		Lower triangle matrix format in case we need to use for solving TSP
		"""
		lt = np.triu(data['distance'])
		return lt
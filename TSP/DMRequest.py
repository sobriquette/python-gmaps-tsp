import requests, os
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from itertools import combinations

class DMRequest(object):
	def __init__(self):
		self.base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
		self.api_key = os.environ['DistanceMatrix_APIKEY']

	def get_distances(self, config):
		"""
		Sends GET request to the Google Distance Matrix API
		"""
		return requests.get(self.base_url, params=config).json()

	def get_response_data(self, places):
		"""
		Parse API response for distance and duration values
		"""
		data = {'waypoints_distances': {}, 'waypoints_durations': {}}

		for (waypoint1, waypoint2) in combinations(places, 2):
			try:
				config = {
					'origins': waypoint1,
					'destinations': waypoint2,
					'key': self.api_key
				}

				response = self.get_distances(config)

				distance = response['rows'][0]['elements'][0]['distance']['value']
				duration = response['rows'][0]['elements'][0]['duration']['value']

				data['waypoints_distances'][frozenset([waypoint1, waypoint2])] = distance
				data['waypoints_durations'][frozenset([waypoint1, waypoint2])] = duration
			
			except Exception as e:
				print("Could not find route from %s to %s." % (waypoint1, waypoint2))

		return data

	@staticmethod
	def build_distance_matrix(data, places):
		"""
		Creates a distance matrix for TSP computation by the Concorde Solver.
		This will be used when we submit a job to the NEOS server.
		"""
		distances = data['distance']

		df = pd.DataFrame(distances, columns=places, index=places)
		dm = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
		return dm

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
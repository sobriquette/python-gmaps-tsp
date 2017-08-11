import requests, os
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

class DMRequest(object):
	def __init__(self, places):
		self.base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
		self.api_key = os.environ['DistanceMatrix_APIKEY']
		self.places = places
		self.config = {
			'origins': '|'.join(self.places['origins']),
			'destinations': '|'.join(self.places['destinations']),
			'key': self.api_key,
		}

	def get_distances(self):
		"""
		Sends GET request to the Google Distance Matrix API
		"""
		return requests.get(self.base_url, params=self.config).json()

	@staticmethod
	def get_response_data(response):
		"""
		Parse API response for distance and duration values
		"""
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
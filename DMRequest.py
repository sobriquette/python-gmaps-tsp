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

	##########################################################
	## GET request to the Google Distance Matrix API 		##
	##########################################################
	def get_matrix(self):
		return requests.get(self.base_url, params=self.config).json()

	##########################################################
	## Parse response for distance and duration values	 	##
	##########################################################
	@staticmethod
	def get_response_data(response):
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

	##########################################################
	## Create a distance matrix for TSP computation		 	##
	##########################################################
	@staticmethod
	def build_distance_matrix(data):
		distances = data['distance']
		durations = data['duration']

		df = pd.DataFrame(distances, columns=places, index=places)
		dm = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
		return dm

	############################################
	## Create a lower triangle matrix for TSP ##
	############################################
	@staticmethod
	def build_lower_triangle_matrix(data):
		lt = np.tril(data['distance'])
		return lt
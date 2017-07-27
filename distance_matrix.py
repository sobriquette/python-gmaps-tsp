import requests, os
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

# make a request to the Gmaps Distance Matrix API
def request_matrix(base_url, config):
	response = requests.get(base_url, params=config).json()
	return response

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

def build_distance_matrix(data, places):
	distances = data['distance']
	durations = data['duration']

	df = pd.DataFrame(distances, columns=places, index=places)
	dm = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
	return dm

def build_lower_triangle_matrix(data):
	lt = np.tril(data['distance'])
	return lt

if __name__ == "__main__":
	base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
	api_key = api_key
	origins = ["Arcadia, CA 91007", "Movie Flat Rd, Lone Pine, CA 93545", "Manzanar Reward Rd, California", "Devils Postpile Access Road, Mammoth Lakes, CA 93546", "Mono Lake, CA"]
	destinations = ["Arcadia, CA 91007", "Movie Flat Rd, Lone Pine, CA 93545", "Manzanar Reward Rd, California", "Devils Postpile Access Road, Mammoth Lakes, CA 93546", "Mono Lake, CA"]
	config = {
		'origins': '|'.join(origins),
		'destinations': '|'.join(destinations),
		'key': api_key,
	}

	response = request_matrix(base_url, config)
	data = get_response_data(response)
	#build_distance_matrix(data, origins)
	distances_lt = build_lower_triangle_matrix(data)
	tsp_template = """
		TYPE : TSP
		DIMENSION: %i
		EDGE_WEIGHT_TYPE : EXPLICIT
		EDGE_WEIGHT_FORMAT : LOWER_DIAG_ROW
		EDGE_WEIGHT_SECTION
		%s
		EOF
	"""

	tsp_data = tsp_template % (5, distances_lt)

	base_xml = """
		<document>
		<category>co</category>
		<solver>concorde</solver>
		<inputType>TSP</inputType>
		<priority>long</priority>
		<email>my-email</email>
		<dat2><![CDATA[]]></dat2>

		<dat1><![CDATA[]]></dat1>

		<tsp><![CDATA[%s]]></tsp>

		<ALGTYPE><![CDATA[con]]></ALGTYPE>

		<RDTYPE><![CDATA[fixed]]></RDTYPE>

		<PLTYPE><![CDATA[no]]></PLTYPE>

		<comment><![CDATA[]]></comment>

		</document>
	"""

	tsp_xml = base_xml % tsp_data
import requests
import os

# build a string to pass into waypoints param 
# of the http request url
def generateWaypointsString(waypoints):
	wp_string = ""
	for i, w in enumerate(waypoints):
		wp_string += w
		if i != (len(waypoints) - 1):
			wp_string += "|"

	return wp_string

# make GET request to google directions api
def getDirections(base_url, config):
	response = requests.get(base_url, params=config).json()
	print(response)
	return response

# take the api response and take only the step-by-step instructions
def getStepsFromDirections(response):
	all_steps = {}

	for r in response['routes']:
		for l in r['legs']:
			for index, s in enumerate(l['steps']):
				all_steps['step-' + str(index)] = s

	return all_steps

# get total driving time
def getTotalDrivingTimes(response):
	total_driving_times = []
	for r in response['routes']:
		for l in r['legs']:
			duration = l['duration']['value']
			total_driving_times.append(duration)

	return total_driving_times

# clean the raw data from the steps dictionary
# keep only the sub-dictionary data we want
def cleanData(steps):
	keep = ['distance', 'duration', 'html_instructions']
	clean = {}

	for step, data in steps.items():
		clean[step] = {}
		for key, val in data.items():
			if str(key) in keep:
				clean[step][key] = val

	return clean

# output data
def printData(data):
	for k,v in data.items():
		print("{}: {}".format(k,v))

# get the optimized order for each waypoint/stopover
def getWaypointOrder(response):
	return response['routes'][0]['waypoint_order']

if __name__ == "__main__":
	# parameters
	base_url = 'https://maps.googleapis.com/maps/api/directions/json'
	optimize_waypoints = 'optimize:true'
	waypoints = [optimize_waypoints,'New York City', 'Washington D.C.']
	config = {'origin': 'Boston', 'destination': 'Myrtle Beach', 
			  'api_key': os.environ['Directions_APIKEY'],
			  'waypoints': generateWaypointsString(waypoints)}

	# make request to GMaps Directions API
	directions = getDirections(base_url, config)
	# pull in all the steps
	raw_steps_data = getStepsFromDirections(directions)
	# clean the raw data
	clean_steps_data = cleanData(raw_steps_data)

	printData(clean_steps_data)
	print(getTotalDrivingTimes(directions))
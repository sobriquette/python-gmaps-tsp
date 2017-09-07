import os, sys, time, re
from xmlrpc import client

class ConcordeResult(object):
	def __init__(self):
		self.NEOS_HOST = "neos-server.org"
		self.NEOS_PORT = 3333
		self.neos = client.ServerProxy('https://%s:%d' % (self.NEOS_HOST, self.NEOS_PORT))

	def create_tsplib_template(self, data):
		"""
			Puts data into TSPLIB format for NEOS/Concorde solver.
			Data must be in lower triangular matrix.
		"""
		tsp_template = """
		TYPE: TSP
		DIMENSION: %d
		EDGE_WEIGHT_TYPE: EXPLICIT
		EDGE_WEIGHT_FORMAT: FULL_MATRIX
		EDGE_WEIGHT_SECTION:
		%s
		EOF
		"""

		# Convert to integers for TSPLIB format
		data_text = '\n'.join(' '.join(map(str, map(int, row))) for row in data)
		return tsp_template % ( len(data), data_text )

	def create_xml_template(self, data):
		"""
			Puts templated data into TSPLIB XML format for NEOS/Concorde solver.
			Base XML template is defined here.
		"""
		base_xml = """
		<document>
		<category>co</category>
		<solver>concorde</solver>
		<inputMethod>TSP</inputMethod>
		<priority>long</priority>
		<email>%s</email>
		<tsp><![CDATA[%s]]></tsp>
		<ALGTYPE><![CDATA[con]]></ALGTYPE>
		<RDTYPE><![CDATA[fixed]]></RDTYPE>
		<PLTYPE><![CDATA[no]]></PLTYPE>
		</document>
		"""

		return base_xml % ( os.environ['email'], self.create_tsplib_template(data) )

	def solve_tsp_with_neos_concorde(self, data):
		"""
			Run and submit job to NEOS server so it can return results
			for the traveling salesman problem
		"""

		# Check that we have data to submit
		if not data:
			raise Exception("No data to submit job with")

		xml = self.create_xml_template(data)

		# Verify connection is successful
		test = self.neos.ping()
		if self.neos.ping() != "NeosServer is alive\n":
			sys.stderr.write("Could not make connection to the NEOS server")
			sys.exit(1)

		if sys.argv[0] == "queue":
			# Print NEOS job queue
			msg = self.neos.printQueue()
			sys.stdout.write(msg)
		else:
			# Submit optimization problem to NEOS
			( jobNumber, password ) = self.neos.submitJob( xml )
			sys.stdout.write( "JobNumber = %d \n" % jobNumber )

			# Check to make sure queue is not full
			if jobNumber == 0:
				sys.stderr.write( "NEOS error: %s" % password )
				sys.exit(1)
			else:
				offset = 0
				status = ""
				while status != "Done":
					( msg, offset ) = self.neos.getIntermediateResults( jobNumber, password, offset )
					sys.stdout.write( msg.data.decode() )
					status = self.neos.getJobStatus( jobNumber, password )

				# Print out final result
				msg = self.neos.getFinalResults( jobNumber, password ).data
				sys.stdout.write( msg.decode() )
				print(msg)
				return msg

	@staticmethod
	def get_tour(num_points, msg, places):
		"""
			Take Concorde results log and parse for city numbers and ranking.
			Put ordering into a list (tour).
		"""
		start_str = '%d %d' % (num_points, num_points)

		# Search the Concorde log for the start of city numbers
		# Get the index where the numbers are first listed
		start = msg.find(start_str)
		legs = msg[( start + len(start_str + 1) ):]
		indices = re.findall(r'(\d+) \d+ \d+', legs)
		tour = map(lambda x: places['destinations'][int(x)], indices)
		tour.append(tour[0])

		print(tour)
		return tour

	@staticmethod
	def create_routes(tour):
		"""
			Code for parameterizing results to render in html.
			Split tour into subtours with a start, end, and waypoints.
		"""
		routes = []
		length = len(tour)
		i = 1

		while length >= 2:
			rlength = min( 8, length - 2 )
			start = tour[0]
			end = tour[rlength + 1]
			route = tour[ 1 : rlength + 1 ]
			routes.append( (i, start, end, route) )
			i += 1
			tour = tour[rlength + 1:]
			length = len(tour)

		print(routes)
		return routes

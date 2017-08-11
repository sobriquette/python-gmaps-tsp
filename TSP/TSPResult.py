import os, sys, time, re
from xmlrpc import client

class TSPResult(object):
	def __init__(self):
		self.NEOS_HOST = "neos-server.org"
		self.NEOS_PORT = 3333
		self.neos = client.ServerProxy('https://%s:%d' % (self.NEOS_HOST, self.NEOS_PORT))
		self.xml = None

	@staticmethod
	def create_tsp_template(n_points, data):
		"""
		Puts data into TSPLIB format for NEOS/Concorde solver.
		Data must be in lower triangular matrix.
		"""
		tsp_template = """
		TYPE : TSP
		DIMENSION: %i
		EDGE_WEIGHT_TYPE : EXPLICIT
		EDGE_WEIGHT_FORMAT : LOWER_DIAG_ROW
		EDGE_WEIGHT_SECTION
		%s
		EOF
		"""

		return tsp_template % ( n_points, data )

	@staticmethod
	def create_xml_template(templated_data):
		"""
		Puts templated data into TSPLIB XML format for NEOS/Concorde solver.
		Base XML template is defined here.
		"""
		base_xml = """
		<document>
		<category>co</category>
		<solver>concorde</solver>
		<inputType>TSP</inputType>
		<priority>long</priority>
		<email>%s</email>
		<dat2><![CDATA[]]></dat2>

		<dat1><![CDATA[]]></dat1>

		<tsp><![CDATA[%s]]></tsp>

		<ALGTYPE><![CDATA[con]]></ALGTYPE>

		<RDTYPE><![CDATA[fixed]]></RDTYPE>

		<PLTYPE><![CDATA[no]]></PLTYPE>

		<comment><![CDATA[]]></comment>

		</document>
		"""

		return base_xml % ( os.environ['email'], templated_data )

	@staticmethod
	def get_xml_with_data(num_points, data):
		"""
		Create XML for NEOS server job using our XML template and templated data.
		"""
		tsp_templated_data = TSPResult.create_tsp_template( num_points, data )
		tsp_xml = TSPResult.create_xml_template( tsp_templated_data )
		return tsp_xml

	def run_tsp_job(self, xml):
		"""
		Run and submit job to NEOS server so it can return results
		for the traveling salesman problem
		"""

		# Check that we have data to submit
		if not xml: 
			return "No job to submit"

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

	def get_tour(num_points, msg, places):
		"""
		Take Concorde results log and parse for city numbers and ranking.
		Put ordering into a list (tour).
		"""

		num_points2 = num_points
		start_str = '%d %d' % (num_points, num_points2)

		# Search the Concorde log for the start of city numbers
		# Get the index where the numbers are first listed
		start = msg.find(start_str)
		legs = msg[( start + len(start_str + 1) ):]
		indices = re.findall(r'(\d+) \d+ \d+', legs)
		tour = map(lambda x: places['destinations'][int(x)], indices)
		tour.append(tour[0])

		print(tour)
		return tour


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

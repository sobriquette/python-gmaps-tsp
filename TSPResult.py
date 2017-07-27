#################################################################################################
## Source: https://www.ibm.com/developerworks/community/blogs/jfp/resource/tsp_nb.html?lang=en ##
#################################################################################################
import os, sys, time
from xmlrpc import client

class TSPResult(object):
	def __init__(self):
		self.NEOS_HOST = "neos-server.org"
		self.NEOS_PORT = 3333
		self.neos = client.ServerProxy('https://%s:%d' % (self.NEOS_HOST, self.NEOS_PORT))
		self.xml = None

	##########################################
	## TSPLIB format for NEOS/Concorde 		##
	## Tempate for lower triangular matrix 	##
	##########################################
	@staticmethod
	def create_tsp_template(n_points, data):
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

	######################################
	## TSPLIB XML for NEOS/Concorde 	##
	## Define base XML template 		##
	######################################
	@staticmethod
	def create_xml_template(templated_data):
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

	######################################
	## Create XML for NEOS server job 	##
	######################################
	@staticmethod
	def get_xml_with_data(num_points, data):
		tsp_templated_data = TSPResult.create_tsp_template( num_points, data )
		tsp_xml = TSPResult.create_xml_template( tsp_templated_data )
		return tsp_xml

	######################
	## Run job on NEOS 	##
	######################
	def run_tsp_job(self, xml):
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

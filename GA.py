from createHTML import create_optimal_route_html, get_route_from_ranking
import random

def compute_fitness(solution, waypoints_distances):
	"""
		We calculate the total distance traveled on this current tour.
		Our GA will favor road trips with shorter total distances traveled.
	"""
	solution_fitness = 0.0

	for index in range(len(solution)):
		waypoint1 = solution[index - 1]
		waypoint2 = solution[index]
		solution_fitness += waypoints_distances[frozenset([waypoint1, waypoint2])]

	return solution_fitness

def generate_random_agent(waypoints):
	"""
		Creates a random road trip from all waypoints
	"""
	new_random_agent = list(waypoints)
	random.shuffle(new_random_agent)
	return tuple(new_random_agent)

def mutate_agent(agent_genome, max_mutations=3):
	"""
		A point mutation swaps the order of 2 waypoints in the tour.
		We apply a number of point mutations in range of 1 - max.
	"""
	agent_genome = list(agent_genome)
	num_mutations = random.randint(1, max_mutations)

	for mutation in range(num_mutations):
		swap_index1 = random.randint(0, len(agent_genome) - 1)
		swap_index2 = swap_index1

		while swap_index1 == swap_index2:
			swap_index2 = random.randint(0, len(agent_genome) - 1)

		agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]

	return tuple(agent_genome)

def shuffle_mutation(agent_genome):
	"""
		Applies a single shuffle mutation to the given tour.
		
		A shuffle mutation takes a random sub-section of the tour
		and moves it to another location in the tour.
	"""
	agent_genome = list(agent_genome)
	
	start_index = random.randint(0, len(agent_genome) - 1)
	length = random.randint(2, 20)
	
	genome_subset = agent_genome[start_index : start_index + length]
	agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]

	insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
	agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

	return tuple(agent_genome)

def generate_random_population(pop_size, waypoints):
	"""
		Generates a list with 'pop_size' number of tours.
	"""
	random_population = []
	for agent in range(pop_size):
		random_population.append(generate_random_agent(waypoints))
	return random_population

def run_genetic_algorithm(places, waypoints_distances, generations=5000, population_size=100):
	"""
		Core of the GA -- 'generations' and 'population_size' must be a multiple of 10.
	"""
	current_best_distance = 1
	population_subset_size = int(population_size // 10)
	generations_10pct = int(generations // 10)

	# Create a random population of 'population_size' number of solutions
	population = generate_random_population(population_size, places)

	# For 'generations' number of repetitions...
	for generation in range(generations):
		# Compute the fitness of the entire current population
		population_fitness = {}

		for agent_genome in population:
			if agent_genome in population_fitness:
				continue

			population_fitness[agent_genome] = compute_fitness(agent_genome, waypoints_distances)

		# Take top 10% shortest tours and produce offspring from each of them
		new_population = []
		for rank, agent_genome in enumerate(sorted(population_fitness, key=population_fitness.get)[:population_subset_size]):
			if (generation % generations_10pct == 0 or generation == generations - 1) and rank == 0:
				current_best_genome = agent_genome
				print("Generation %d | best: %d | Unique genomes: %d" % (generation, population_fitness[agent_genome], len(population_fitness)))
				print(agent_genome)
				print("")

			# If this is the first route found, or it is shorter than the best route we know,
			# create a html output and display it
			if population_fitness[agent_genome] < current_best_distance or current_best_distance < 0:
				current_best_distance = population_fitness[agent_genome]
				create_optimal_route_html(agent_genome, current_best_distance, False)

			# Create 1 exact copy of each of the top tours
			new_population.append(agent_genome)

			# Create 2 offspring with 1-3 point mutations
			for offspring in range(2):
				new_population.append(mutate_agent(agent_genome, 3))

			# Create 7 offspring with a single shuffle mutation
			for offspring in range(7):
				new_population.append(shuffle_mutation(agent_genome))

			# Replace the old population with new population of offspring
			# for i in range(len(population))[::-1]:
			# 	del population[i]

			population = new_population

	return current_best_genome
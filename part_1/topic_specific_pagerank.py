import utils.pagerank_utils as pru

default_alpha = .15
default_epsilon = 10**-6


########################################################################################
########################################################################################
########################################################################################


def compute_topic_specific_pagerank(graph, teleporting_distribution=None, alpha=default_alpha, epsilon=default_epsilon):
	"""
	Compute the pagerank of a graph, with a given teleporting distribution over all the nodes (it is used for manage some topic-based pagerank)
	:param graph: a Weighted Undirected Graph. Some remarks:
	 	- each EDGE has a field "weight"
	 	- each NODE has a field "edge_weight_sum", which represents the sum of the weights of their edges.
	:param teleporting_distribution: a teleporting distribution over all the nodes
	:param alpha: the damping factor
	:param epsilon: affects the convergence condition
	:return: a dictionary {node_id: score}
	"""

	if teleporting_distribution==None:
		teleporting_distribution = pru.get_uniform_teleporting_distribution(graph)

	previous_page_rank_vector = create_initial_pagerank_vector(graph)
	page_rank_vector = {}
	num_iterations = 0

	while True:

		# Compute next pagerank vector
		page_rank_vector = single_iteration_topic_specific_page_rank(graph, previous_page_rank_vector, alpha=alpha, teleporting_distribution=teleporting_distribution)

		num_iterations += 1

		# Evaluate the distance between the old and new pagerank vectors

		previous_page_rank_vector_values = [t[1] for t in sorted(previous_page_rank_vector.items(), key=lambda x: x[0])]
		page_rank_vector_values = [t[1] for t in sorted(page_rank_vector.items(), key=lambda x: x[0])]
		distance = get_distance(previous_page_rank_vector_values, page_rank_vector_values)

		# print(num_iterations)

		# Check for convergence
		if distance <= epsilon:
			# print()
			# print(" Convergence!")
			# print()
			break

		previous_page_rank_vector = page_rank_vector

	return page_rank_vector


def create_initial_pagerank_vector(graph):
	page_rank_vector = {}
	num_nodes = graph.number_of_nodes();

	for node in graph:
		page_rank_vector[node] = (1. / num_nodes);

	return page_rank_vector



def single_iteration_topic_specific_page_rank(graph, page_rank_vector, teleporting_distribution=None, alpha=default_alpha):
	if teleporting_distribution==None:
		teleporting_distribution = pru.get_uniform_teleporting_distribution(graph)


	next_page_rank_vector = {}

	num_nodes = graph.number_of_nodes()
	r = {}

	for node in graph:
		r[node] = 0.

		for neighbor in graph[node]:
			weight = graph[node][neighbor]["weight"]
			weight_sum = graph.node[neighbor]["edge_weight_sum"]

			r[node] += (1 - alpha) * page_rank_vector[neighbor] * weight / weight_sum

	# compute the leakedPR subtracting all the computed scores
	leakedPR = 1.
	for node in graph:
		leakedPR -= r[node]

	for node in graph:
		# next_page_rank_vector[node] = r[node]
		# next_page_rank_vector[node] += leakedPR/ topic.number_of_nodes()

		# above two lines in one: I deleted the for-loop on topic nodes.
		next_page_rank_vector[node] = r[node] + leakedPR * teleporting_distribution[node]

	return next_page_rank_vector


def get_distance(vector_1, vector_2):
	distance = 0.

	for v1, v2 in zip(vector_1, vector_2):
		distance += abs(v1 - v2)

	return distance


########################################################################################
########################################################################################
########################################################################################

def print_graph(graph):

	print()
	print("Graph")
	for node in graph:
		print(str(node) + " -- " + str(graph[node]))
	print()





def get_reverse_graph(graph):
	return graph.reverse(copy=True)





########################################################################################
########################################################################################
########################################################################################





### Useful code for debugging ;)
'''
print
print "start PR"
damping_factor = 1. - alpha
pr = nx.pagerank(g, alpha=damping_factor, tol=epsilon)
print "end PR"
print
pp.pprint(pr)
print
print
distance = get_distance(page_rank_vector, pr)
print " distance(just_implemented_pr, NetworkX_pr)= " + str(distance)
print
'''

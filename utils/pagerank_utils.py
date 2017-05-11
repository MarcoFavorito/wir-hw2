import networkx as nx
import csv

def read_movie_graph(input_file_name):

	# Get graph file
	input_file = open(input_file_name, 'r')
	input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)


	# Initialize graph
	graph = nx.Graph()

	# Create graph
	for line in input_file_csv_reader:
		node_1 = int(line[0])
		node_2 = int(line[1])
		weight = int(line[2])

		if not graph.has_node(node_1):
			graph.add_node(node_1, edge_weight_sum=0.)

		if not graph.has_node(node_2):
			graph.add_node(node_2, edge_weight_sum=0.)

		if not graph.has_edge(node_1, node_2):
			graph.add_edge(node_1, node_2, weight=weight)
			graph.node[node_1]["edge_weight_sum"] += weight
			graph.node[node_2]["edge_weight_sum"] += weight

	input_file.close()

	return graph


def read_user_movie_rating(input_file_name):

	input_file = open(input_file_name, "r")
	input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

	user_ratings = {}

	for line in input_file_csv_reader:
		user_id = int(line[0])
		movie_id = int(line[1])
		rating = int(line[2])

		if user_id not in user_ratings:
			user_ratings[user_id] = []

		user_ratings[user_id].append((movie_id, rating))

	return user_ratings

def read_category_movies(input_file_name):
	"""
	Parse the category-movies file
	:param input_file_name: a file where each line is the set of movies for one category
	:return: a dictionary {category_id: [category_movies]}
	"""
	input_file = open(input_file_name, "r")
	input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

	categories = {}
	for i, line in enumerate(input_file_csv_reader):
		# enumerate from 1 to 5 (hence i+1)
		categories[i] = list(map(int, line))

	return categories


def get_uniform_teleporting_distribution(graph):
	"""
	Compute the teleporting distribution, without assumption (i.e. uniform distribution)
	:param graph:
	:return: a dictionary {node_id: 1/|V| }
	"""
	try:
		teleporting_distribution = dict(zip(graph.nodes(), [1/graph.number_of_nodes()]*graph.number_of_nodes()))
	except ZeroDivisionError:
		teleporting_distribution = {}
	return teleporting_distribution


def get_uniform_teleporting_distribution_on_subgraph(graph, subgraph):
	"""
	Compute the teleporting distribution ONLY on a subgraph (i.e. other nodes are set to zero)
	:param graph:
	:return: a dictionary {node_id: 1/|V| }
	"""
	try:
		teleporting_distribution = dict(zip(graph.nodes(), [1/graph.number_of_nodes()]*graph.number_of_nodes()))
	except ZeroDivisionError:
		teleporting_distribution = {}

	complement_nodes = set(graph.nodes()) - set(subgraph.nodes())
	for n in complement_nodes:
		assert n in subgraph.nodes()


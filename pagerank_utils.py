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
			user_ratings[user_id] = {}

		user_ratings[user_id][movie_id] = rating

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
		categories[i+1] = list(map(int, line))

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
		nb_subgraph_nodes = subgraph.number_of_nodes()
		teleporting_distribution = dict(zip(subgraph.nodes(), [1/nb_subgraph_nodes]*nb_subgraph_nodes))
	except ZeroDivisionError:
		# the subgraph has no node... Are you kidding me, ya?
		teleporting_distribution = {}

	# set the probability to zero for the complement of the subgraph
	complement_nodes = set(graph.nodes()) - set(subgraph.nodes())
	for n in complement_nodes:
		# assert n not in subgraph.nodes()
		teleporting_distribution[n]= 0

	return teleporting_distribution


def print_pagerank_list(ids_scores, file=None):
	for id, score in ids_scores:
		print("{0}\t{1}".format(id, score), file=file)


def load_pagerank_vector_from_file(filepath):
	with open(filepath) as fin:
		lines = fin.readlines()
		splitted_lines = map(lambda x: x.split('\t'), lines)
		parsed_lines = map(lambda x: (int(x[0]), float(x[1])), splitted_lines)

	result = dict(parsed_lines)
	return result


def merge_distributions(dist_list, weights):
	assert len(dist_list)==len(weights)
	result = {}
	# normalize weights if they are not
	if sum(weights)!=1.:
		weights = [w/sum(weights) for w in weights]

	for distribution, weight in zip(dist_list, weights):
		for id in distribution:
			if id in result:
				result[id] += distribution[id]*weight
			else:
				result[id] = distribution[id]*weight

	return result

def normalize(d):
	s = sum(d.values())
	return dict((k, v / s) for k, v in d.items())

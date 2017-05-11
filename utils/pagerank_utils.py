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


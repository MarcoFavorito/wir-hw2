import csv
import pprint as pp
import networkx as nx
import matplotlib.pyplot as plt

# input_graph_adjacency_list_file_name = '../../Lab_2_new/small_graph__adjacency_list.tsv'
# input_graph_adjacency_list_file_name = '../../Lab_2_new/wiki_graph__adjacency_list.tsv'

movie_graph_path = "./datasets/movie_graph.txt"
user_movie_rating_path = "./datasets/user_movie_rating.txt"

alpha = .15
epsilon = 10**-6


########################################################################################
########################################################################################
########################################################################################

# def compute_pagerank(graph, reverse_graph):
#
# 	previous_page_rank_vector = create_initial_pagerank_vector(graph)
# 	page_rank_vector = []
# 	num_iterations = 0
#
# 	while True:
#
# 		# pp.pprint(previous_page_rank_vector)
#
# 		# Compute next pagerank vector
# 		page_rank_vector = single_iteration_page_rank(graph, reverse_graph, previous_page_rank_vector, alpha)
#
# 		num_iterations += 1
#
# 		# Evaluate the distance between the old and new pagerank vectors
# 		distance = get_distance(previous_page_rank_vector, page_rank_vector)
#
# 		# print()
# 		# print(" iteration number " + str(num_iterations))
# 		# print(" distance= " + str(distance))
#
# 		# Check for convergence
# 		if distance <= epsilon:
# 			print()
# 			print(" Convergence!")
# 			print()
# 			break
#
# 		previous_page_rank_vector = page_rank_vector
#
# 	# pp.pprint(page_rank_vector)
# 	return page_rank_vector


def compute_pagerank(graph):

	previous_page_rank_vector = create_initial_pagerank_vector(graph)
	page_rank_vector = {}
	num_iterations = 0

	while True:

		# Compute next pagerank vector
		page_rank_vector = single_iteration_page_rank(graph, previous_page_rank_vector, alpha)

		num_iterations += 1

		# Evaluate the distance between the old and new pagerank vectors
		previous_page_rank_vector_values = [t[1] for t in sorted(previous_page_rank_vector.items(), key=lambda x: x[0])]
		page_rank_vector_values = [t[1] for t in sorted(page_rank_vector.items(), key=lambda x: x[0])]
		distance = get_distance(previous_page_rank_vector_values, page_rank_vector_values)

		print(num_iterations)

		# Check for convergence
		if distance <= epsilon:
			print()
			print(" Convergence!")
			print()
			break

		previous_page_rank_vector = page_rank_vector

	return page_rank_vector


def compute_topic_specific_pagerank(graph, topic):

	previous_page_rank_vector = create_initial_pagerank_vector(graph)
	page_rank_vector = {}
	num_iterations = 0

	while True:

		# Compute next pagerank vector
		page_rank_vector = single_iteration_topic_specific_page_rank(graph, topic, previous_page_rank_vector, alpha)

		num_iterations += 1

		# Evaluate the distance between the old and new pagerank vectors

		previous_page_rank_vector_values = [t[1] for t in sorted(previous_page_rank_vector.items(), key=lambda x: x[0])]
		page_rank_vector_values = [t[1] for t in sorted(page_rank_vector.items(), key=lambda x: x[0])]
		distance = get_distance(previous_page_rank_vector_values, page_rank_vector_values)

		print(num_iterations)

		# Check for convergence
		if distance <= epsilon:
			print()
			print(" Convergence!")
			print()
			break

		previous_page_rank_vector = page_rank_vector

	return page_rank_vector


def create_initial_pagerank_vector(graph):
	page_rank_vector = {}
	num_nodes = graph.number_of_nodes();

	for node in graph:
		page_rank_vector[node] = (1. / num_nodes);

	return page_rank_vector


# def single_iteration_page_rank(graph, reverse_graph, page_rank_vector, alpha):
# 	next_page_rank_vector = []
#
# 	num_nodes = len(graph)
# 	r = []
# 	for j in graph:
# 		r.append(0.)
#
# 		for i in reverse_graph[j]:
# 			r[j] += (1 - alpha) * page_rank_vector[i] / len(graph[i])
#
# 	leakedPR = 1.
# 	for j in range(num_nodes):
# 		leakedPR -= r[j]
#
# 	for j in range(num_nodes):
# 		next_page_rank_vector.append(r[j] + leakedPR / num_nodes)
#
# 	return next_page_rank_vector


def single_iteration_page_rank(graph, page_rank_vector, alpha):
	next_page_rank_vector = {}

	num_nodes = graph.number_of_nodes()
	r = {}

	for node in graph:
		r[node] = 0.

		for neighbor in graph[node]:

			weight = graph[node][neighbor]["weight"]
			weight_sum = graph.node[neighbor]["edge_weight_sum"]

			r[node] += (1 - alpha) * page_rank_vector[neighbor] * weight / weight_sum

	leakedPR = 1.
	for node in graph:
		leakedPR -= r[node]

	for node in graph:
		next_page_rank_vector[node] = (r[node] + leakedPR / num_nodes)

	return next_page_rank_vector


def single_iteration_topic_specific_page_rank(graph, topic, page_rank_vector, alpha):
	next_page_rank_vector = {}

	num_nodes = graph.number_of_nodes()
	r = {}

	for node in graph:
		r[node] = 0.

		for neighbor in graph[node]:
			weight = graph[node][neighbor]["weight"]
			weight_sum = graph.node[neighbor]["edge_weight_sum"]

			r[node] += (1 - alpha) * page_rank_vector[neighbor] * weight / weight_sum

	leakedPR = 1.
	for node in graph:
		leakedPR -= r[node]

	for node in graph:
		next_page_rank_vector[node] = r[node]

	bias_sum = 0.
	for node in topic:
		bias_sum += topic.node[node]["bias"]

	for node in topic:
		next_page_rank_vector[node] += leakedPR * topic.node[node]["bias"] / bias_sum

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


# def read_graph_from_file(file_name):
#
# 	# Get graph file
# 	input_file = open(file_name, 'r')
# 	input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
#
#
# 	# Initialize graph
# 	graph = nx.DiGraph()
#
# 	# Create graph
# 	for node__adjacency_list in input_file_csv_reader:
# 		graph.add_node(int(node__adjacency_list[0]))
# 		for adjacent in node__adjacency_list[1:]:
# 			graph.add_edge(*[int(node__adjacency_list[0]), int(adjacent)])
#
# 	input_file.close()
#
# 	return graph


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


def get_topic_from_user_ratings(graph, user_ratings, user_id):

	movie_ratings = user_ratings[user_id]
	movies = []
	for (movie, rating) in movie_ratings:
		movies.append(movie)

	movie_ratings_dict = dict(movie_ratings)
	# pp.pprint(movies)

	topic = graph.subgraph(movies)
	for node in topic:
		topic.node[node]["bias"] = movie_ratings_dict[node]

	return topic


def get_reverse_graph(graph):
	return graph.reverse(copy=True)





########################################################################################
########################################################################################
########################################################################################

def __main():

	print("Reading " + movie_graph_path + "...")
	graph = read_movie_graph(movie_graph_path)
	print("Done!")
	print()
	print("Reading " + user_movie_rating_path + "...")
	user_ratings = read_user_movie_rating(user_movie_rating_path)
	print("Done!")
	print()

	topic = get_topic_from_user_ratings(graph, user_ratings, 1683)
	pp.pprint(topic.nodes())
	for node in topic:
		print(topic.node[node]["bias"])

	# print_graph(graph)

	# Compute PageRank
	# page_rank_vector = compute_pagerank(graph, reverse_graph)
	# page_rank_vector = compute_pagerank(graph)
	# pp.pprint(page_rank_vector)
	# pp.pprint(graph.nodes()[0])
	# pp.pprint(graph.degree(graph.nodes()[0]))


	# nx.draw(graph)
	# plt.show()


__main()





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

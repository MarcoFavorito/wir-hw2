import unittest

from networkx import Graph

import topic_specific_pagerank as TSPageRank
from pagerank_utils import read_movie_graph
import pagerank_utils as pru

default_delta = 1e-05

class test_pagerank(unittest.TestCase):

	def test_pagerank_empty(self):
		# Test if an empty dict is returned for an empty graph
		G = Graph()
		self.assertEqual(TSPageRank.compute_topic_specific_pagerank(G, G), {})

	def test_pagerank_cycle_one_topic(self):
		print("cycle")
		# Test if all nodes in a cycle graph have the same value

		G = read_movie_graph("graphs/graph-01-cycle")

		topic = G.subgraph([1,2,3,4,5])
		uniform_teleporting_distribution = pru.get_uniform_teleporting_distribution(G)

		expected_pr = {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2}
		pr = TSPageRank.compute_topic_specific_pagerank(G, teleporting_distribution=uniform_teleporting_distribution)

		for k in pr:
			self.assertAlmostEqual(pr[k], expected_pr[k], delta=default_delta)

	def test_pagerank_cycle_two_nodes_one_topic(self):
		print("two_nodes_one_topic")
		# Test if all nodes in a cycle graph have the same value

		G = read_movie_graph("graphs/graph-02-two_nodes")

		topic = G.subgraph([1, 2])
		teleporting_distribution = {1:0.5, 2:0.5}
		expected_pr = {1: 0.5, 2: 0.5}
		pr = TSPageRank.compute_topic_specific_pagerank(G, teleporting_distribution=teleporting_distribution)

		for k in pr:
			self.assertAlmostEqual(pr[k], expected_pr[k], delta=default_delta)

	def test_pagerank_cycle_two_nodes_two_topic(self):
		print("two_nodes_two_topic")
		# Test if all nodes in a cycle graph have the same value

		G = read_movie_graph("graphs/graph-02-two_nodes")

		topic = G.subgraph([2])
		expected_pr = {1: 0.4594592532498197, 2: 0.5405407467501804}
		teleporting_distribution = {1:0.0, 2:1.0}

		pr = TSPageRank.compute_topic_specific_pagerank(G, teleporting_distribution=teleporting_distribution)

		for k in pr:
			self.assertAlmostEqual(pr[k], expected_pr[k], delta=default_delta)
#
	#
	# def test_pagerank(self):
	# 	# Test example from wikipedia: http://en.wikipedia.org/wiki/File:Linkstruct3.svg
	# 	G = Graph()
	# 	G.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
	# 	G.add_edge(1, 2, weight=1.)
	# 	G.add_edge(1, 3, weight=1.)
	# 	G.add_edge(1, 4, weight=1.)
	# 	G.add_edge(1, 5, weight=1.)
	# 	G.add_edge(1, 7, weight=1.)
	# 	G.add_edge(2, 1, weight=1.)
	# 	G.add_edge(3, 1, weight=1.)
	# 	G.add_edge(3, 2, weight=1.)
	# 	G.add_edge(4, 2, weight=1.)
	# 	G.add_edge(4, 3, weight=1.)
	# 	G.add_edge(4, 5, weight=1.)
	# 	G.add_edge(5, 1, weight=1.)
	# 	G.add_edge(5, 3, weight=1.)
	# 	G.add_edge(5, 4, weight=1.)
	# 	G.add_edge(5, 6, weight=1.)
	# 	G.add_edge(6, 1, weight=1.)
	# 	G.add_edge(6, 5, weight=1.)
	# 	G.add_edge(7, 5, weight=1.)
	# 	expected_pagerank = {
	# 		1: 0.280,
	# 		2: 0.159,
	# 		3: 0.139,
	# 		4: 0.108,
	# 		5: 0.184,
	# 		6: 0.061,
	# 		7: 0.069,
	# 	}
	# 	pr = compute_pagerank(G)
	# 	for k in pr:
	# 		self.assertAlmostEqual(pr[k], expected_pagerank[k], places=3)
	#
#
# 	def test_pagerank_random(self):
# 		pass
# 		# G = testlib.new_DiGraph()
# 		# md = 0.00001
# 		# df = 0.85
# 		# pr = compute_pagerank(G)
# 		# min_value = (1.0 - df) / len(G)
# 		# for node in G:
# 		# 	expected = min_value
# 		# 	for each in G.incidents(node):
# 		# 		expected += (df * pr[each] / len(G.neighbors(each)
# 		# 	assert abs(pr[node] - expected) < md
#

if __name__ == "__main__":
	unittest.main()

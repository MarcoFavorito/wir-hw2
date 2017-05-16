import unittest
import networkx as nx
from networkx import Graph
import random
from pagerank_utils import read_movie_graph
import pagerank_utils as pru
import topic_specific_pagerank as tspr

default_delta = 1e-05

class test_pagerank(unittest.TestCase):

	def test_pagerank_empty(self):
		# Test if an empty dict is returned for an empty graph
		G = Graph()
		self.assertEqual(tspr.compute_topic_specific_pagerank(G, G), {})

	def test_pagerank_cycle_one_topic(self):
		# print("cycle")
		# Test if all nodes in a cycle graph have the same value

		G = read_movie_graph("graphs/graph-01-cycle")

		topic = G.subgraph([1,2,3,4,5])
		uniform_teleporting_distribution = pru.get_uniform_teleporting_distribution(G)

		expected_pr = {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2}
		pr = tspr.compute_topic_specific_pagerank(G, teleporting_distribution=uniform_teleporting_distribution)

		for k in pr:
			self.assertAlmostEqual(pr[k], expected_pr[k], delta=default_delta)

	def test_pagerank_cycle_two_nodes_one_topic(self):
		# print("two_nodes_one_topic")
		# Test if all nodes in a cycle graph have the same value

		G = read_movie_graph("graphs/graph-02-two_nodes")

		topic = G.subgraph([1, 2])
		teleporting_distribution = {1:0.5, 2:0.5}
		expected_pr = {1: 0.5, 2: 0.5}
		pr = tspr.compute_topic_specific_pagerank(G, teleporting_distribution=teleporting_distribution)

		for k in pr:
			self.assertAlmostEqual(pr[k], expected_pr[k], delta=default_delta)

	def test_pagerank_cycle_two_nodes_two_topic(self):
		# print("two_nodes_two_topic")
		# Test if all nodes in a cycle graph have the same value

		G = read_movie_graph("graphs/graph-02-two_nodes")

		topic = G.subgraph([2])
		expected_pr = {1: 0.4594592532498197, 2: 0.5405407467501804}
		teleporting_distribution = {1:0.0, 2:1.0}

		pr = tspr.compute_topic_specific_pagerank(G, teleporting_distribution=teleporting_distribution)

		for k in pr:
			self.assertAlmostEqual(pr[k], expected_pr[k], delta=default_delta)

	def test_pagerank_with_networkx(self):
		g = pru.read_movie_graph("datasets/movie_graph.txt")
		random_distribution = dict([(n, random.random()) for n in g.nodes()])
		norm_random_distribution = pru.normalize(random_distribution)

		# we need a stronger precision in order to compare both the pageranks!
		epsilon = 1e-12

		pr_expected = nx.pagerank(g, personalization=norm_random_distribution, tol=epsilon)
		pr_computed = tspr.compute_topic_specific_pagerank(g, norm_random_distribution, epsilon=epsilon)

		# compare the number of keys
		self.assertEqual(set(pr_expected), set(pr_computed))

		# compare the values for each key
		for k in pr_computed:
			# try with delta=1e-18...
			self.assertAlmostEqual(pr_computed[k], pr_expected[k], delta=1e-06)

		# compare the order of the pagerank
		list_pr_expected = sorted(pr_expected.items(), key=lambda x: -x[1])
		list_pr_computed = sorted(pr_computed.items(), key=lambda x: -x[1])

		# print(sum(a[1] for a in list_pr_expected))
		# print(sum(a[1] for a in list_pr_computed))

		for i,(a,b) in enumerate(zip(list_pr_computed, list_pr_expected)):
			# print(i, a, b, a[1]-b[1])
			self.assertEqual(a[0], b[0])
			self.assertAlmostEqual(a[1], b[1], delta=1e-06)

		pass
	

if __name__ == "__main__":
	unittest.main()

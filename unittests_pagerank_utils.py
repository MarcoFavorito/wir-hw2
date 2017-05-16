import unittest

import networkx as nx
from functools import reduce
import pagerank_utils as pru

GRAPH_DIR = "./graphs/"

class test_pagerank_utils(unittest.TestCase):
	def test_graph_cycle(self):
		graph_path = GRAPH_DIR + "graph-01-cycle"
		G = pru.read_movie_graph(graph_path)

		G_test = nx.Graph()
		G_test.add_nodes_from([1,2,3,4,5])
		G_test.add_edge(1, 2, weight=1.)
		G_test.add_edge(2, 3, weight=1.)
		G_test.add_edge(3, 4, weight=1.)
		G_test.add_edge(4, 5, weight=1.)
		G_test.add_edge(5, 1, weight=1.)

		assert G_test.__eq__(G)

	def test_merge_distributions(self):
		d1 = {'a':1.0, 'b':2.0}
		d2 = {'b':3.0, 'c':5.0}
		d3 = {'d':10.0}
		d_list = [d1,d2,d3]


		def keys(dict_list):
			return reduce(lambda a,b: a.union(b), dict_list, set())

		norm_dicts = list(map(pru.normalize, d_list))
		reduced_dict = reduce(
			lambda a, b: {k: a.get(k,0.0) + b.get(k,0.0) for k in set(a).union(b)},
			norm_dicts
		)
		norm_reduced_dict = pru.normalize(reduced_dict)

		computed_result = pru.merge_distributions(norm_dicts, [1,1,1])
		print(norm_reduced_dict)
		print(computed_result)

		self.assertEqual(set(norm_reduced_dict), set(computed_result))
		for k in norm_reduced_dict:
			# try with delta=1e-18... It fails.
			self.assertAlmostEqual(norm_reduced_dict[k], computed_result[k], delta=1e-16)



if __name__ == '__main__':
	unittest.main()

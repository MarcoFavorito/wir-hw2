import unittest

import networkx as nx

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



if __name__ == '__main__':
	unittest.main()

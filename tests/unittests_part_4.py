import unittest
import part_2.WebIR_HW_2_part_2 as p2
import part_4.WebIR_HW_2_part_4 as p4
import os
import utils.pagerank_utils as pru

class test_part_4(unittest.TestCase):

	def setUp(self):
		self.dataset_movie_graph = "../datasets/movie_graph.txt"
		self.dataset_user_movie_rating = "../datasets/user_movie_rating.txt"
		self.userid = 1683

	def test_merge_one_user(self):
		"""
		python WebIR_HW_2_part_4.py ../datasets/movie_graph.txt ../datasets/user_movie_rating.txt 1683_1
		Run part_4 with a group of one user
		It should be equal to the output of homework two, using the same user.
		:return:
		"""
		movie_graph_path = self.dataset_movie_graph
		user_ratings_path = self.dataset_user_movie_rating

		users_weights_pairs = {self.userid: 2}

		movie_graph = pru.read_movie_graph(movie_graph_path)

		user_ratings = pru.read_user_movie_rating(user_ratings_path)

		group_ratings = dict([(userid, user_ratings[userid]) for userid in users_weights_pairs])

		# from part 4
		filtered_group_pagerank = p4._pagerank_from_group_ratings(movie_graph, group_ratings, users_weights_pairs)
		# from part 2
		filtered_single_user_pagerank = p2._pagerank_from_user_ratings(movie_graph, user_ratings[self.userid])

		# group (single-user) pagerank
		sorted_and_filtered_group_pagerank = sorted(filtered_group_pagerank, key=lambda x: -x[1])
		# single user pagerank
		sorted_filtered_single_user_pagerank = sorted(filtered_single_user_pagerank, key=lambda x: -x[1])

		self.assertEqual(sorted_and_filtered_group_pagerank, sorted_filtered_single_user_pagerank)





if __name__ == '__main__':
	unittest.main()

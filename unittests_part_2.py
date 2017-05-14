import unittest
import WebIR_HW_2_part_2 as p2
import os
# import WebIR_HW_2_part_2 as hw2_2
import pagerank_utils as pru

class test_part_2(unittest.TestCase):

	def setUp(self):
		self.dataset_movie_graph = "./datasets/movie_graph.txt"
		self.dataset_user_movie_rating = "./datasets/user_movie_rating.txt"



	def test_ratings_top_bottom(self):
		self.first_six_el_list = [
			(423, 0.0024930517122088813),
			(405, 0.002429449144203104),
			(294, 0.0024044963439005043),
			(288, 0.0023852167636827953),
			(318, 0.0022338594396764224),
			(286, 0.002204159897947397)
		]

		self.last_six_el_list = [
			(1309, 2.775025022327991e-06),
			(1618, 2.1959487041917455e-06),
			(1235, 2.1692001153129452e-06),
			(1236, 2.1692001153129452e-06),
			(1671, 2.0399563817660503e-06),
			(1653, 1.3627268273044816e-06)
		]

		userid = 1683

		# read the whole movie graph from its adjacency list
		movie_graph = pru.read_movie_graph(self.dataset_movie_graph)

		# retrieve ALL user ratings (we can improve it reading only those line of our userid):
		user_ratings = pru.read_user_movie_rating(self.dataset_user_movie_rating)

		# we have a dictionary {userid: [(movie_id, rating)]}
		# get the list of ratings of only our user:
		cur_user_ratings = user_ratings[userid]
		# get the set of movies_id: it will be used for filtering the recommendations
		rated_movies = set([m for m in cur_user_ratings.keys()])

		filtered_movies_scores = p2._pagerank_from_user_ratings(movie_graph, cur_user_ratings)

		sorted_and_filtered_movies_scores = sorted(filtered_movies_scores, key=lambda x: -x[1])


		self.assertEqual(self.first_six_el_list, sorted_and_filtered_movies_scores[:6])
		self.assertEqual(self.last_six_el_list, sorted_and_filtered_movies_scores[-6:])


	# def test_compare(self):pass




if __name__ == '__main__':
	unittest.main()

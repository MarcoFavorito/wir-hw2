import unittest
import part_2.WebIR_HW_2_part_2 as p2
import os
# import WebIR_HW_2_part_2 as hw2_2
import utils.pagerank_utils as pru

class test_part_2(unittest.TestCase):
	def test_ratings(self):
		# first_six_el = {
		# 	423: 0.0024930517122088813,
		# 	405: 0.002429449144203104,
		# 	294: 0.0024044963439005043,
		# 	288: 0.0023852167636827953,
		# 	318: 0.0022338594396764224,
		# 	286: 0.002204159897947397
		# }

		first_six_el_list = [
			(423, 0.0024930517122088813),
			(405, 0.002429449144203104),
			(294, 0.0024044963439005043),
			(288, 0.0023852167636827953),
			(318, 0.0022338594396764224),
			(286, 0.002204159897947397)
		]
# 		output_six_el = '''423	0.0024930517122088813
# 405	0.002429449144203104
# 294	0.0024044963439005043
# 288	0.0023852167636827953
# 318	0.0022338594396764224
# 286	0.002204159897947397'''

		dataset_movie_graph ="../datasets/movie_graph.txt"
		dataset_user_movie_rating = "../datasets/user_movie_rating.txt"
		userid = 1683

		# read the whole movie graph from its adjacency list
		movie_graph = pru.read_movie_graph(dataset_movie_graph)

		# retrieve ALL user ratings (we can improve it reading only those line of our userid):
		user_ratings = pru.read_user_movie_rating(dataset_user_movie_rating)

		# we have a dictionary {userid: [(movie_id, rating)]}
		# get the list of ratings of only our user:
		cur_user_ratings = user_ratings[userid]

		self.assertEqual(first_six_el_list, p2._recommend_movies(movie_graph, cur_user_ratings)[:6])

	def test_compare(self):
		dataset_movie_graph = "../datasets/movie_graph.txt"
		dataset_user_movie_rating = "../datasets/user_movie_rating.txt"
		userid = 1683



if __name__ == '__main__':
	unittest.main()

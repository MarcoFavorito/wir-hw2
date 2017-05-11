import unittest
import part_2.WebIR_HW_2_part_2 as p2
import os

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
		self.assertEqual(first_six_el_list, p2._reccomend_movies(dataset_movie_graph, dataset_user_movie_rating, userid)[:6])


if __name__ == '__main__':
	unittest.main()

import unittest
import part_2.WebIR_HW_2_part_2 as p2
import part_3.WebIR_HW_2_part_3_online as p3_online
import os
import utils.pagerank_utils as pru
import configurations as conf

class test_part_3(unittest.TestCase):
	def setUp(self):
		self.topic_based_pageranks = p3_online._load_precomputed_categories_pageranks([1,1,1,1,1])

	def test_merge_one_weight(self):
		preference_vector_one_weight = [1., 0., 0., 0., 0.]
		merged_scores = p3_online._recommend_movies_multi_category(preference_vector_one_weight)

		merged_scores_sorted = sorted(merged_scores.items(), key=lambda x: -x[1])
		topic_pagerank_sorted = sorted(self.topic_based_pageranks[0].items(), key=lambda x: -x[1])
		for (a,b),(c,d) in zip(merged_scores_sorted, topic_pagerank_sorted):
			self.assertEqual((a,b), (c,d))
		# self.assertEqual(merged_scores, self.topic_based_pageranks[1])

	def test_merge_top_bottom(self):
		preference_vector = [1.,2,3., 4., 5.]

		first_six = [
			(50, 0.0034744157088306845),
			(181, 0.0031707208742270446),
			(100, 0.00308350404711971),
			(174, 0.003002478357484924),
			(121, 0.002833388691257197),
			(98, 0.0028163326568209535)
		]

		last_six = [
			(1596, 2.8659415422330017e-05),
			(1433, 2.8374541891874553e-05),
			(1122, 2.8357280009580206e-05),
			(1614, 2.4974386099998458e-05),
			(1654, 2.35690576867756e-05),
			(1156, 2.3526898446109754e-05)
		]
		merged_scores = p3_online._recommend_movies_multi_category(preference_vector)

		merged_scores_sorted = sorted(merged_scores.items(), key=lambda x: -x[1])

		self.assertEqual(merged_scores_sorted[:6], first_six)
		self.assertEqual(merged_scores_sorted[-6:], last_six)


if __name__ == '__main__':
	unittest.main()

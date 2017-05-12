import sys

import part_1.topic_specific_pagerank as tspr
import utils.pagerank_utils as pru

verbose = False


def _print_usage():
	usage='''
Usage:
	python WebIR_HW_2_part_2.py <graph_path> <user_ratings> <user_id> [--verbose]
Example:
	python WebIR_HW_2_part_2.py ../datasets/movie_graph.txt ../datasets/user_movie_rating.txt 1683 --verbose
	'''
	print(usage)

def main():

	if len(sys.argv)>=4:
		movie_graph_path = sys.argv[1]
		user_ratings_path = sys.argv[2]
		userid = int(sys.argv[3])

		if len(sys.argv)==5 and sys.argv[4]=="--verbose": verbose=True
	else:
		_print_usage()
		exit(1)


	# read the whole movie graph from its adjacency list
	movie_graph = pru.read_movie_graph(movie_graph_path)

	# retrieve ALL user ratings (we can improve it reading only those line of our userid):
	users_ratings = pru.read_user_movie_rating(user_ratings_path)

	# we have a dictionary {userid: [(movie_id, rating)]}
	# get the list of ratings of only our user:
	user_ratings = users_ratings[userid]


	movies_scores = _pagerank_from_user_ratings(movie_graph, user_ratings, verbose=verbose)

	sorted_and_filtered_movies_scores = sorted(movies_scores, key=lambda x: -x[1])

	pru.print_pagerank_list(sorted_and_filtered_movies_scores)

	return sorted_and_filtered_movies_scores

def _pagerank_from_user_ratings(movie_graph, user_ratings, verbose=False):
	"""

	:param movie_graph_path:
	:param user_ratings_path:
	:param userid:
	:param verbose:
	:return:
	"""


	# get the set of ALL movies_ids: it will be used for set their teleporting probability to zero
	all_movies = set(movie_graph.nodes())

	# get the set of movies_id: it will be used for filtering the recommendations
	rated_movies = set([m for m in user_ratings.keys()])


	# compute teleporting distribution from the set of ratings (with biasing, as explained in the homework)
	teleporting_distribution = _compute_teleport_distribution_from_ratings(user_ratings, all_movies)

	# compute the pagerank as in part 1. It returns a dictionay {movie_id: score}
	movie_scores = tspr.compute_topic_specific_pagerank(movie_graph, teleporting_distribution=teleporting_distribution)

	# filter from the obtained list the movies already seen
	filtered_movies_scores = filter(lambda x: x[0] not in rated_movies, movie_scores.items())

	return filtered_movies_scores



def _compute_teleport_distribution_from_ratings(user_rating, all_movies):
	"""
	returns the teleporting distribution as explained in the homework
	if a movie M has been rated, its probability is: RATE_M / SUM_OF_ALL_RATINGS
	else, its probability is: 0
	:param user_rating: a dict of (movie_id, rating)
	:param all_movies: a set of movie ids, either rated or not. It is used for filter
			the movies that have no rating, and then their probability will be set to 0.
	:return:
	"""
	distribution = {}
	rating_sum = sum(user_rating.values())
	for movie_id, rating in user_rating.items():
		distribution[movie_id]=rating/rating_sum
	for not_rated_movie in filter(lambda x: x not in distribution, all_movies):
		distribution[not_rated_movie] = 0

	return distribution





if __name__ == '__main__':
	main()

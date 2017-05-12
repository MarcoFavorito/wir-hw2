import sys
import configurations as conf
import utils.pagerank_utils as pru
from _functools import reduce
import part_1.topic_specific_pagerank as tspr
import part_2.WebIR_HW_2_part_2 as part2

def _print_usage():
	usage='''Usage:
	python WebIR_HW_2_part_4.py <graph_path> <user_ratings> <user_group_weights> [--verbose]
Example:
	python WebIR_HW_2_part_4.py ../datasets/movie_graph.txt ../datasets/user_movie_rating.txt 1683_1__1684_2 --verbose
	'''
	print(usage)

def main():

	if len(sys.argv)>=4 and len(sys.argv)<=5:
		movie_graph_path = sys.argv[1]
		user_ratings_path = sys.argv[2]
		users_weights_pairs = dict([(int(user.split('_')[0]), int(user.split('_')[1])) for user in sys.argv[3].split('__')])

		if len(sys.argv)==5 and sys.argv[4]=="--verbose": verbose=True
	else:
		_print_usage()
		exit(1)

	# read the whole movie graph from its adjacency list
	movie_graph = pru.read_movie_graph(movie_graph_path)

	# retrieve ALL user ratings (we can improve it reading only those line of our userid):
	user_ratings = pru.read_user_movie_rating(user_ratings_path)

	# we have a dictionary {userid: [(movie_id, rating)]}
	# get the list of ratings of the group, i.e. from every user.
	# at the end we have a dict: {userid: {movie_id: rate}}
	group_ratings = dict([(userid, user_ratings[userid]) for userid in users_weights_pairs])

	# compute the pagerank of the group from the group ratings
	filtered_group_pagerank = _pagerank_from_group_ratings(movie_graph, group_ratings, users_weights_pairs)

	# sort by score
	sorted_and_filtered_group_pagerank = sorted(filtered_group_pagerank, key=lambda x: -x[1])

	pru.print_pagerank_list(sorted_and_filtered_group_pagerank)

	return sorted_and_filtered_group_pagerank


def _pagerank_from_group_ratings(movie_graph, group_ratings, users_weights_pairs, verbose=False):
	all_movies = movie_graph.nodes()

	merged_teleporting_distribution = {}
	users_distributions = []

	for userid in group_ratings:
		cur_userrating = group_ratings[userid]
		users_distributions.append(part2._compute_teleport_distribution_from_ratings(cur_userrating, all_movies))

	# list comprehension on user_weights_pairs, instead of .values(), for preserve order (?)
	merged_teleporting_distribution = pru.merge_distributions(users_distributions, [w for _, w in users_weights_pairs.items()])

	# compute pagerank from the resulting distribution
	group_pagerank = tspr.compute_topic_specific_pagerank(movie_graph, merged_teleporting_distribution)

	# compute all the movies seen from the group: it is used for filtering
	all_seen_movies_from_group = set([m for seen_movies_one_user in group_ratings.values() for m in seen_movies_one_user.keys()])

	# filter the result with the already seen film
	filtered_final_pagerank = filter(lambda x: x[0] not in all_seen_movies_from_group, group_pagerank.items())

	return filtered_final_pagerank

if __name__ == '__main__':
	main()
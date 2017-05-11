import utils.pagerank_utils as pru
import part_1.topic_specific_pagerank as tspr
import pprint as pp
import configurations as conf

def compute_pageranks_by_category(movie_graph, category_movies_dict):
	"""
	From a movie graph and a dictionary {category_id : [movie_ids]}
	compute |C| pageranks, where C is the set of cotegories (i.e. the set of lines)
	In other words, execute |C| times (the number of categories) the pagerank algorithm
	topic-based (i.e. the teleporting probability distribution is positive and uniform only
	on movie belonging to the category of a given iteration, while the p.m.f. is zero over the
	rest of movies)
	:param movie_graph_filepath:
	:param category_movies_filepath:
	:return:
	"""
	result = {}

	categories = category_movies_dict.keys()

	for category_id in categories:
		# get
		cur_category_subgraph = movie_graph.subgraph(category_movies_dict[category_id])

		# uniform distribution ONLY on movies belonging to the category; probabilities for other movies are set to zero.
		cur_teleporting_distribution = pru.get_uniform_teleporting_distribution_on_subgraph(movie_graph, cur_category_subgraph)

		# compute pagerank on the entire movie_graph for the current category (i.e. the current teleporting p.m.f)
		cur_pagerank = tspr.compute_topic_specific_pagerank(movie_graph, teleporting_distribution=cur_teleporting_distribution)

		# sort by score
		cur_pagerank_sorted = sorted(cur_pagerank.items(), key=lambda x: -x[1])

		# store the result in the result dictionary
		result[category_id] = cur_pagerank_sorted

	return result


def main(movie_graph_filepath, category_movies_filepath, output_dir):
	"""
	Compute the pagerank topic-based over every category and save each list of tuple (movie_id, score)
	in files which filepath is "${output_dir}/pagerank_${category_id}"
	:param movie_graph_filepath:
	:param category_movies_filepath:
	:param output_dir:
	:return:
	"""

	movie_graph = pru.read_movie_graph(movie_graph_filepath)
	category_movies_dict = pru.read_category_movies(category_movies_filepath)


	category2pagerank = compute_pageranks_by_category(movie_graph, category_movies_dict)


	for category_id in category2pagerank:
		output_filepath = conf.PART_2_OUTPUT_DIR + conf.PART_2_PAGERANK_OUTPUT_FILENAME_FORMAT
		output_filepath = output_filepath.format(category_id)
		with open(output_filepath, "w") as fout:
			pru.print_pagerank_list(category2pagerank[category_id], file=fout)



if __name__ == '__main__':
	movie_graph_filepath = conf.DATA_DIR + conf.MOVIE_GRAPH_FILENAME
	category_movies_filepath = conf.DATA_DIR + conf.CATEGORY_MOVIES_FILENAME
	output_dir = conf.PART_2_OUTPUT_DIR

	main(movie_graph_filepath, category_movies_filepath, output_dir)




import utils.pagerank_utils as pru
import part_1.topic_specific_pagerank as tspr

def compute_pageranks_by_category(movie_graph_filepath, category_movies_filepath, output_directory):
	movie_graph = pru.read_movie_graph(movie_graph_filepath)
	category_movies_dict = pru.read_category_movies(category_movies_filepath)

	categories = category_movies_dict.keys()

	for c in categories:
		teleporting_distribution = pru.get_uniform_teleporting_distribution()
		tspr.compute_topic_specific_pagerank(movie_graph,)
	pass


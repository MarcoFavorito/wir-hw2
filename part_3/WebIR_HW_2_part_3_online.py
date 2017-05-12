import sys
import configurations as conf
import utils.pagerank_utils as pru
from _functools import reduce

def _print_usage():
	usage='''Usage:
	python WebIR_HW_2_part_3_online.py <preferences-vector> [--verbose]
Example:
	python WebIR_HW_2_part_3_online.py 3_4_0_1_1 --verbose'''
	print(usage)

def main():

	if len(sys.argv)>=2 and len(sys.argv)<=3:
		preference_vector = [int(pref) for pref in sys.argv[1].split('_')]

		if len(sys.argv)==3 and sys.argv[2]=="--verbose": verbose=True
	else:
		_print_usage()
		exit(1)

	# the dictionary id2score for store the merged score
	merged_scores = _recommend_movies_multi_category(preference_vector)

	# sort the merged_scores by score (descending)
	sorted_merged_scores = sorted(merged_scores.items(), key=lambda x: -x[1])

	# print on stdout
	pru.print_pagerank_list(sorted_merged_scores)

	return sorted_merged_scores


def _recommend_movies_multi_category(preference_vector):
	# the dictionary id2score for store the merged score
	merged_scores = {}

	# normalize preference_vector
	norm = sum(preference_vector)
	norm_preference_vector = [pref/norm for pref in preference_vector]

	# list of topic-based pageranks; we will combine them with the weights in input
	# enumerate categories from 1
	# for each category, load its topic-based pagerank
	topic_based_pageranks = _load_precomputed_categories_pageranks(norm_preference_vector)

	# merge all the keys of the pagerank vectors (i.e.: all the involved movie_ids in the merge)
	ids_union = set(reduce(lambda x, y: x.union(y), [set(d.keys()) for d in topic_based_pageranks]))

	# merge distribution works (it seems to...) also for pageranks ;)
	# Below the older version, before the implementation of "merge_distributions" used for part 4.
	merged_scores = pru.merge_distributions(topic_based_pageranks, norm_preference_vector)

	# OLD VERSION
	# # for every id, sum its scores for every pagerank category (zero if that movie is not present)
	# for id in ids_union:
	# 	# for a single id:
	# 	# 1) iterate over the involved categories
	# 	# 2) for each category, compute its contribution (if present) for the current id, weighting that value
	# 	# 3) sum all the contributions
	# 	merged_scores[id] = sum([norm_weight*cur_tbpr.get(id, 0) for (cur_tbpr, norm_weight) in zip(topic_based_pageranks, norm_preference_vector)])

	return merged_scores


def _load_precomputed_categories_pageranks(norm_preference_vector):
	result = []
	for category_id in range(1, len(norm_preference_vector)+1):
		if norm_preference_vector[category_id-1]==0:
			result.append({})
			continue
		CUR_CATEGORY_PAGERANK_FILEPATH = conf.PART_2_OUTPUT_DIR + conf.PART_2_PAGERANK_OUTPUT_FILENAME_FORMAT
		CUR_CATEGORY_PAGERANK_FILEPATH = CUR_CATEGORY_PAGERANK_FILEPATH.format(category_id)

		cur_pagerank_vector = pru.load_pagerank_vector_from_file(CUR_CATEGORY_PAGERANK_FILEPATH)
		result.append(cur_pagerank_vector)

	return result


if __name__ == '__main__':
    main()
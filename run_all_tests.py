from unittest import TestLoader, TextTestRunner, TestSuite
import unittests_pagerank
import unittests_pagerank_utils
import unittests_part_2
import unittests_part_3
import unittests_part_4

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(unittests_pagerank.test_pagerank),
		loader.loadTestsFromTestCase(unittests_pagerank_utils.test_pagerank_utils),
		loader.loadTestsFromTestCase(unittests_part_2.test_part_2),
		loader.loadTestsFromTestCase(unittests_part_3.test_part_3),
		loader.loadTestsFromTestCase(unittests_part_4.test_part_4)
	))

    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)

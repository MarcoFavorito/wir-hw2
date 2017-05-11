from unittest import TestLoader, TextTestRunner, TestSuite
import tests.unittests_pagerank
import tests.unittests_pagerank_utils
import tests.unittests_part_2

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(tests.unittests_pagerank.test_pagerank),
		loader.loadTestsFromTestCase(tests.unittests_pagerank_utils.test_pagerank_utils),
		loader.loadTestsFromTestCase(tests.unittests_part_2.test_part_2)
        ))

    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
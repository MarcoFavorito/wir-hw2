import sys

def _print_usage():
	usage='''
Usage:
	python WebIR_HW_2_part_3_online.py USER_ID preferences-vector [--verbose]
Example:
	python WebIR_HW_2_part_3_online.py 1683 3_4_0_1_1 --verbose
	'''
	print(usage)

def main():

	if len(sys.argv)>=3:
		userid = sys.argv[1]
		preference_vector = [int(pref) for pref in sys.argv[2].split('_')]

		if len(sys.argv)==4 and sys.argv[3]=="--verbose": verbose=True
	else:
		_print_usage()
		exit(1)



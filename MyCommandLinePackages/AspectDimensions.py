# Author		:	Md. Shahedul Islam Shahed
# Language		:	python 3.5
# Concise		: 	Calculates aspect ratio and dimensions


import argparse
import math


def main():
	parser = argparse.ArgumentParser(description="Get aspect dimensions (lenth and width).")

	parser.add_argument('-d', '--diag-len', dest='diag_len', metavar='LEN', default=5, type=float, help='The length of display diagonal. Default is %(default)s units.')
	parser.add_argument('-r', '--aspect-ratio', dest='asp_rat', metavar='N', nargs=2, type=float, default=(16, 9), help="The display aspect ratio in form of <r1 r2> meaning the ratio r1:r2. Default is 16:9. Example: -r 16 9 which means 16:9.")

	args = parser.parse_args()
	
	diag = args.diag_len
	r1, r2 = args.asp_rat

	if diag <= 0 or r1 <= 0 or r2 <= 0:
		print("Invalid argument.")
		parser.print_help()
		exit()

	b = diag * r2 / math.sqrt(r1*r1 + r2*r2)
	a = r1 * b / r2

	print("Diagonal length   : %g unit" % (diag))
	print("Aspect ratio      : %g:%g\nthen" % (r1, r2))
	print("Aspect dimensions : %g unit, %g unit" % (a, b))


if __name__ == '__main__':
	main()

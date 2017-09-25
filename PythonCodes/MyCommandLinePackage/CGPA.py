import argparse


def grade_credit(val):
	print("Val: ", val)
	L = val.split()
	return (str(L[0], float(L[1])))


def main():
	parser = argparse.ArgumentParser(description="Calculate your CGPA.")

	parser.add_argument('-n', dest='tot_sub', type=int, required=True, metavar='N', help="Number of subjects.")

	parser.add_argument('-g', dest='letter_grades', metavar='LETTER_GRADE', nargs='+', type=str, choices=('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F'), help="Letter grade of the subjects.")
	parser.add_argument('-c', dest='credits', metavar='CREDIT', nargs='+', type=float, help="Credit of the subjects respectively.")

	args = parser.parse_args()

	if len(args.letter_grades) != args.tot_sub or len(args.credits) != args.tot_sub:
		print("There must be exactly %d letter grades with letter points." % (args.tot_sub))
		exit()

	grade_table = {'A+': 4.00,
				'A': 3.75,
				'A-': 3.50,
				'B+': 3.25,
				'B': 3.00,
				'B-': 2.75,
				'C+': 2.50,
				'C': 2.25,
				'D': 2.00,
				'F': 0.00}

	s = 0
	tot_credit = 0
	cnt = 1

	print("Subject   Letter grade   Credit\n-------   ------------   ------")

	for grade, credit in zip(args.letter_grades, args.credits):
		print("%5d. %11s %11.2f" % (cnt, grade, credit))
		s += grade_table[grade] * credit
		tot_credit += credit
		cnt += 1

	print("                         ------")
	print("                          %d (Total credit)" % (tot_credit))

	print("Your CGPA %.2f" % (s / tot_credit))


if __name__ == '__main__':
	main()
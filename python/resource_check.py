#! /usr/bin/python3

import resource
import sys

def main():
	sys.setswitchinterval(2)

	for i in range(10000):
		for j in range(10000):
			pass

	ru = resource.getrusage(resource.RUSAGE_SELF)
	print(ru.ru_utime, ru.ru_stime, ru.ru_maxrss)

if __name__ == '__main__':
	main()

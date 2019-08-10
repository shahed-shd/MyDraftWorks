# ==================================================
# Problem   :
# Run time  :    sec.
# Language  :   Python 3.5
# ==================================================


import sys


def main():
    sys.stdin = open("in.txt", "r")
    sys.stdout = open("out.txt", "w")

    it = iter(map(int, sys.stdin.read().split()))
    ansL = [str(x) for x in it]

    print("Hello World!")

    sys.stdout.write(''.join(ansL))


if __name__ == '__main__':
    main()
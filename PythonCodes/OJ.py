#! /usr/bin/python3

# ==================================================
# Problem   :   Ugly Numbers
# Run time  :   35 /35
# Language  :   Python 3
# ==================================================


def main():
    from sys import stdin, stdout

    # stdin = open("in.txt", "r")

    it = iter(map(int, stdin.read().split()))

    n = next(it)
    m = next(it)

    mn = min(n, m)
    rem = n + m - 2 * mn
    # ans = 0

    if mn <= rem:
        ans = mn
    else:
        ans = rem
        ans += ((mn - rem) // 3) * 2

    stdout.write(str(ans) + '\n')


if __name__ == '__main__':
    main()

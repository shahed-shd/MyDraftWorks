#! /usr/bin/python3

# ==================================================
# Problem  :   12289 - One-Two-Three
# Run time :   0.010 sec.
# Language :   Python 3.5
# ==================================================


from collections import deque


def bfs(adjList):
    q = deque()
    n = len(adjList)
    vis = [False] * n

    q.append(0)
    vis[0] = True

    while True:
        try:
            u_idx = q.popleft()
        except:
            break

        for v_idx in adjList[u_idx]:
            if not vis[v_idx]:
                vis[v_idx] = True;
                q.append(v_idx)

    return (False not in vis)


def form_adjList(stations):
    n = len(stations)
    adjList = [[] for _ in range(n)]
    INF = 123456789

    for i in range(n):
        u = stations[i]
        d1 = d2 = INF; idx1 = idx2 = INF

        for j in range(n):
            if i == j: continue

            v = stations[j]
            d = (u[0] - v[0]) * (u[0] - v[0]) + (u[1] - v[1]) * (u[1] - v[1])

            if d < d1:
                d2 = d1; idx2 = idx1
                d1 = d; idx1 = j
            elif d == d1:
                old_v = stations[idx1]

                if old_v[0] > v[0] or (old_v[0] == v[0] and old_v[1] > v[1]):
                    d2 = d1; idx2 = idx1
                    idx1 = j;
            elif d < d2:
                d2 = d; idx2 = j
            elif d == d2:
                old_v = stations[idx2]

                if old_v[0] > v[0] or (old_v[0] == v[0] and old_v[1] > v[1]):
                    idx2 = j

        adjList[i].append(idx1)
        adjList[i].append(idx2)

    return adjList


def main():
    from sys import stdin, stdout

    # stdin = open("in.txt", "r")

    it = iter(stdin.read().split())
    ans = []

    while True:
        n = int(next(it))
        if not n:
            break

        stations = []

        for _ in range(n):
            stations.append((int(next(it)), int(next(it))))

        adjList = form_adjList(stations)
        
        ans.append("All stations are reachable.\n" if bfs(adjList) else "There are stations that are unreachable.\n")

    stdout.write(''.join(ans))


if __name__ == '__main__':
    main()

// ==================================================
// Problem  :   10687 - Monitoring the Amazon
// Run time :   0.020 sec.
// Language :   C++11
// ==================================================

#include <cstdio>
#include <queue>
#include <vector>
#include <climits>
using namespace std;


typedef     pair<int, int>      ii;

const int INF = INT_MAX;

vector<vector<ii> > adjList;


void dijkstra(int s, int n)
{
    priority_queue<ii, vector<ii>, greater<ii> > pq;
    int dist[n+3];
    fill(dist, dist+n+1, INF);

    pq.push(ii(0, s));
    dist[s] = 0;

    while(!pq.empty()) {
        int u = pq.top().second; pq.pop();

        for(auto &pr : adjList[u]) {
            int v = pr.first;
            int w = pr.second;

            if(dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push(ii(dist[v], v));
            }
        }
    }

    int mxDist1 = -1, mxDist2 = -1, node1, node2;

    for(int i = 1; i <= n; ++i) {
        if(mxDist1 <= dist[i]) {
            mxDist2 = mxDist1, node2 = node1;
            mxDist1 = dist[i], node1 = i;
        }
        else if(mxDist2 < dist[i]) {
            mxDist2 = dist[i], node2 = i;
        }
    }

    if(mxDist1 == mxDist2) {
        for(auto &pr : adjList[node1]) {
            if(pr.first == node2) {
                printf("The last domino falls after %.1f seconds, between key dominoes %d and %d.\n", mxDist1+pr.second/2.0, node1, node2);
                return;
            }
        }
    }

    printf("The last domino falls after %.1f seconds, at key domino %d.\n", double(mxDist1), node1);
}


int main()
{
    freopen("in.txt", "r", stdin);

    int n, m;

    while(scanf("%d %d", &n,  &m), n and m) {
        adjList.clear();

        adjList.resize(n+3);

        int u, v, w;

        while(m--) {
            scanf("%d %d %d", &u, &v, &w);
            adjList[u].push_back(ii(v, w));
            adjList[v].push_back(ii(u, w));
        }

        dijkstra(1, n);
    }

    return 0;
}

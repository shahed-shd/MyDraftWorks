// ==================================================
// Problem  :   894E - Ralph and Mushrooms
// Run time :   1.075 sec.
// Language :   C++11
// ==================================================

// SCC and DAG - Tarjan's algorithm
// Time Complexity  : O(V+E)

#include <cstdio>
#include <bitset>
#include <stack>
#include <vector>
using namespace std;


const int MAXN = 10 + 3;

vector<vector<int> > adjList, adj;
vector<int> sccId;

vector<int> disc, low;
stack<int> stk;
bitset<MAXN> isInStack;
int sccCnt, timeCnt;


void tarjan_scc(int u)
{
    disc[u] = low[u] = ++timeCnt;
    stk.push(u);
    isInStack[u] = true;

    for(auto &v: adjList[u]) {
        if(disc[v] == -1) {
            tarjan_scc(v);
            low[u] = min(low[u], low[v]);
        }
        else if(isInStack[v]) {
            low[u] = min(low[u], disc[v]);
        }
    }

    if(disc[u] == low[u]) {
        int tp;

        do {
            tp = stk.top(); stk.pop();
            isInStack[tp] = false;
            sccId[tp] = sccCnt;
        } while(tp != u);

        ++sccCnt;
    }
}


int main()
{
    //freopen("in.txt", "r", stdin);

    int n = 6;

    adjList.resize(n+3);

    adjList[0].push_back(1);
    adjList[1].push_back(2);
    adjList[2].push_back(3);
    adjList[3].push_back(4);
    adjList[4].push_back(2);
    adjList[5].push_back(1);
    adjList[5].push_back(4);

    // SCC

    sccId.assign(n+3, -1);

    disc.assign(n+3, -1);
    low.assign(n+3, -1);
    isInStack.reset();
    sccCnt = 0;
    timeCnt = 0;

    for(int i = 0; i < n; ++i)
        if(disc[i] == -1)
            tarjan_scc(i);

    printf("Total SCC: %d\n", sccCnt);

    for(int i = 0; i < n; ++i)
        printf("node %d is in scc %d\n", i, sccId[i]);

    // Constructing DAG

    adj.resize(sccCnt+3);

    for(int u = 0; u < n; ++u) {
        for(auto &v : adjList[u]) {
            int uu = sccId[u], vv = sccId[v];
            if(uu != vv)
                adj[uu].push_back(vv);
        }
    }

    printf("\nNow, the DAG:\n");

    for(int u = 0; u < sccCnt; ++u) {
        printf("%d ->", u);
        for(auto &v : adj[u])
            printf(" %d", v);
        putchar('\n');
    }

    return 0;
}

/*
Output:
--------------------
Total SCC: 4
node 0 is in scc 2
node 1 is in scc 1
node 2 is in scc 0
node 3 is in scc 0
node 4 is in scc 0
node 5 is in scc 3

Now, the DAG:
0 ->
1 -> 0
2 -> 1
3 -> 1 0
--------------------
*/

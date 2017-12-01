// ==================================================
// Problem  :   894C - Marco and GCD Sequence
// Run time :   0.015 sec.
// Language :   C++11
// ==================================================

#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

typedef     long long       LL;

const int MAXN = 1e6 + 3;

int n, L[MAXN];
vector<int> distances[MAXN];
vector<LL> cum_sum[MAXN];


LL get_ans(int a, LL h)
{
    LL ret = h;

    int cnt = upper_bound(distances[a].begin(), distances[a].end(), h) - distances[a].begin();
    if(cnt) ret += cnt * h - cum_sum[a][cnt-1];

    int u, v = a;

    while(h > 0) {
        u = v / 2;

        if(u == 0) break;

        if(L[v-1] <= h) {
            ret +=  h - L[v-1];
            h -= L[v-1];
        }
        else break;

        if(h == 0) break;

        int v2 = (v & 1)? v-1 : v+1;

        if(v2 <= n and L[v2-1] <= h) {
            ret += h - L[v2-1];

            cnt = upper_bound(distances[v2].begin(), distances[v2].end(), h - L[v2-1]) - distances[v2].begin();
            if(cnt) ret += cnt * (h - L[v2-1]) - cum_sum[v2][cnt-1];
        }

        v = u;
    }

    return ret;
}


void dfs_merge(int u)
{
    int v1 = u << 1, v2 = (u << 1) | 1;
    auto &dist_u = distances[u], &dist_v1 = distances[v1], &dist_v2 = distances[v2];;

    if(v1 <= n) dfs_merge(v1), dist_u.push_back(L[v1-1]);
    if(v2 <= n) dfs_merge(v2), dist_u.push_back(L[v2-1]);

    if(dist_u.size() == 2 and dist_u[0] > dist_u[1])
        swap(dist_u[0], dist_u[1]);

    int sz1 = distances[v1].size(), sz2 = distances[v2].size();

    for(int i = 0, j = 0; i < sz1 or j < sz2; ) {
        if(i < sz1 and (j >= sz2 or dist_v1[i] < dist_v2[j]))
            dist_u.push_back(L[v1-1] + dist_v1[i++]);
        else
            dist_u.push_back(L[v2-1] + dist_v2[j++]);
    }

    auto &cum_sum_u = cum_sum[u];

    for(auto &x : dist_u)
        cum_sum_u.push_back(cum_sum_u.size() ? cum_sum_u.back() + x : x);
}

int main()
{
    //freopen("in.txt", "r", stdin);

    ios::sync_with_stdio(false);

    int m;
    cin >> n >> m;

    for(int i = 1; i < n; ++i) cin >> L[i];

    dfs_merge(1);

    int a, h;

    while(m--) {
        cin >> a >> h;
        cout << get_ans(a, h) << '\n';
    }

    return 0;
}

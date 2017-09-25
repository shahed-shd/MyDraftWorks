#include <iostream>
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5;

int arr[N+1] {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

class segmentTree {
    vector<int> tree;

public:
    segmentTree(int n) {
        int x = ceil(log2(n));
        int mx = 2 * int(pow(2, x)) - 1;
        tree.resize(mx+1);
    }

    void init(int node, int s, int t) {
        if(s == t) {
            tree[node] = arr[s];
            return;
        }

        int left = node+node, right = left+1, mid = (s+t)/2;

        init(left, s, mid);
        init(right, mid+1, t);

        tree[node] = tree[left] + tree[right];
    }

    int query(int node, int s, int t, int rs, int rt) {
        if(s > rt || t < rs)
            return 0;

        if(s >= rs && t <= rt)
            return tree[node];

        int left = node+node, right = left+1, mid = (s+t)/2;

        int p1 = query(left, s, mid, rs, rt);
        int p2 = query(right, mid+1, t, rs, rt);

        return p1 + p2;
    }

    void update(int node, int s, int t, int idx, int val) {
        if(idx < s || idx > t)
            return;

        if(s == t) {    // if(i <= s && i >= t)
            tree[node] = val;
            return;
        }

        int left = node+node, right = left+1, mid = (s+t)/2;

        update(left, s, mid, idx, val);
        update(right, mid+1, t, idx, val);

        tree[node] = tree[left] + tree[right];
    }
};


int main()
{
    segmentTree ob(N);

    ob.init(1, 1, N);

    cout << ob.query(1, 1, N, 1, 4) << '\n';

    ob.update(1, 1, N, 4, 5);

    cout << ob.query(1, 1, N, 1, 4) << '\n';

    return 0;
}

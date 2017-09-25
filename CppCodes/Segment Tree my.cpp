#include <cstdio>
#include <vector>
#include <cmath>
using namespace std;

const int MAXN = 1e5 + 3;

int arr[MAXN] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

class segmentTree {
    vector<int> propagate;
    vector<int> tree;

public:
    segmentTree(int n) {
        int x = ceil(log2(n));
        int mx = 2 * int(pow(2, x)) - 1;
        tree.resize(mx+1);
        propagate.assign(mx+1, 0);
    }

    void init(int node, int s, int t) {
        if(s == t) {
            tree[node] = arr[s];
            return;
        }

        int left = node<<1, right = (node<<1)|1, mid = (s+t)>>1;

        init(left, s, mid);
        init(right, mid+1, t);

        tree[node] = tree[left] + tree[right];
    }

    void update(int node, int s, int t, int rs, int rt, int addVal) {
        if(t < rs || rt < s) return;
        if(rs <= s && t <= rt) {
            propagate[node] += addVal;
            return;
        }

        int left = node<<1, right = (node<<1)|1, mid = (s+t)>>1;

        update(left, s, mid, rs, rt, addVal);
        update(right, mid+1, t, rs, rt, addVal);

        tree[node] = tree[left] + propagate[left] * (mid - s + 1) + tree[right] + propagate[right] *(t - (mid+1) +1);
    }

    int query(int node, int s, int t, int rs, int rt, int lazy = 0) {
        if(t < rs || rt < s) return 0;
        if(rs <= s && t <= rt) return tree[node] + (propagate[node]+lazy) * (t-s+1);

        int left = node<<1, right = (node<<1)|1, mid = (s+t)>>1;

        int p1 = query(left, s, mid, rs, rt, lazy+propagate[node]);
        int p2 = query(right, mid+1, t, rs, rt, lazy+propagate[node]);

        return p1 + p2;
    }
};

int main()
{
    int n = 10;
    segmentTree ob(10);

    ob.init(1, 1, n);

    printf("%d\n", ob.query(1, 1, n, 1, 10));

    printf("%d\n", ob.query(1, 1, n, 1, 7));

    ob.update(1, 1, n, 4, 6, 10);

    printf("%d\n", ob.query(1, 1, n, 1, 7));

    return 0;
}


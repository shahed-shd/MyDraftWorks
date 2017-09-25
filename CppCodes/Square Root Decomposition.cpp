// Data Structure   : Square Root Decomposition.
// Related Problem  : LightOJ 1082 - Array Queries

#include <cstdio>
#include <vector>
#include <climits>
#include <cmath>
using namespace std;

const int MAXN = 1e5+3;

class sqrtDecomposition {
    int bucketSize;
    vector<int> buckets;

public:
    sqrtDecomposition(int n) {
        bucketSize = sqrt(n);
        buckets.assign(bucketSize+1, INT_MAX);
    }

    void init(int arr[], int sz) {
        for(int i = 0; i < sz; ++i)
            buckets[i/bucketSize] = min(buckets[i/bucketSize], arr[i]);
    }

    int query(int arr[], int s, int t) {
        int bucketStart = s/bucketSize, bucketEnd = t/bucketSize;

        int mn = INT_MAX;

        if(bucketStart == bucketEnd) {
            for(int i = s; i <= t; ++i)
                mn = min(mn, arr[i]);

            return mn;
        }

        int tmp = (bucketStart+1) * bucketSize;

        for(int i = s; i < tmp; ++i) mn = min(mn, arr[i]);
        for(int i = bucketStart+1; i < bucketEnd; ++i) mn = min(mn, buckets[i]);
        for(int i = bucketEnd*bucketSize; i <= t; ++i) mn = min(mn, arr[i]);

        return mn;
    }
};

int main()
{
    //freopen("in", "r", stdin);

    int t;
    scanf("%d", &t);

    for(int tc = 1; tc <= t; ++tc) {
        int n, q;
        scanf("%d %d", &n, &q);

        int arr[n+3];

        for(int i = 0; i < n; ++i)
            scanf("%d", arr+i);

        sqrtDecomposition sd(n);

        sd.init(arr, n);

        printf("Case %d:\n", tc);

        while(q--) {
            int a, b;
            scanf("%d %d", &a, &b);

            printf("%d\n", sd.query(arr, a-1, b-1));
        }
    }

    return 0;
}

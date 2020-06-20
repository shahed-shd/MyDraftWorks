// for max/min : https://sites.google.com/site/shymaalgo/structs/sqrt-decomposition


// Program to compute sum of ranges for different range queries.
#include <bits/stdc++.h>
using namespace std;

int block;  // Variable to represent block size. This is made global, so compare() of sort can use it.

struct Query    // Structure to represent a query range.
{
    int L, R;
};

bool compare(Query x, Query y)                  // Function used to sort all queries so that all queries
{                                               // of same block are arranged together and within a block,
    // Different blocks, sort by block.         // queries are sorted in increasing order of R values.
    if (x.L/block != y.L/block)
        return x.L/block < y.L/block;

    // Same block, sort by R value
    return x.R < y.R;
}

void queryResults(int a[], int n, Query q[], int m)         // Prints sum of all query ranges. m is number of queries. n is size of array a[].
{

    block = (int)sqrt(n);               // Find block size

    sort(q, q + m, compare);            // Sort all queries so that queries of same blocks are arranged together.

    int currL = 0, currR = 0;           // Initialize current L, current R and current sum.
    int currSum = 0;

    for (int i=0; i<m; i++) {           // Traverse through all queries.
        int L = q[i].L, R = q[i].R;     // L and R values of current range.

        while (currL < L) {             // Remove extra elements of previous range.
            currSum -= a[currL];        // For example if previous range is [0, 3] and
            currL++;                    // current range is [2, 5], then a[0] and a[1] are subtracted.
        }

        while (currL > L) {             // Add Elements of current Range.
            currSum += a[currL-1];
            currL--;
        }
        while (currR <= R) {
            currSum += a[currR];
            currR++;
        }

        while (currR > R+1) {           // Remove elements of previous range.
            currSum -= a[currR-1];      // For example when previous range is [0, 10] and current range
            currR--;                    // is [3, 8], then a[9] and a[10] are subtracted.
        }

        cout << "Sum of [" << L << ", " << R << "] is "  << currSum << endl;    // Print sum of current range
    }
}

// Driver program
int main()
{
    int a[] = {1, 1, 2, 1, 3, 4, 5, 2, 8};

    int n = sizeof(a)/sizeof(a[0]);

    Query q[] = {{0, 4}, {1, 3}, {2, 4}};

    int m = sizeof(q)/sizeof(q[0]);

    cout << "Index: ";
    for(int i = 0; i < n; ++i)
        cout << ' ' << i;

    cout << "\nArray: ";
    for(int i = 0; i < n; ++i)
        cout << ' ' << a[i];

    cout << "\n\n";

    queryResults(a, n, q, m);

    return 0;
}

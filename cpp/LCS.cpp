#include <iostream>
#include <algorithm>
using namespace std;

#define VISOK

string a, b;
string nxt;
int len_a, len_b, dp[10][10];

#ifdef VISOK
bool vis[10][10] = {false};
#endif // VISOK

int lcs(int ia, int ib)
{
    if(ia == len_a || ib == len_b) return 0;

    if(dp[ia][ib] != -1) return dp[ia][ib];

    int ret;

    if(a[ia] == b[ib]) ret = 1 + lcs(ia+1, ib+1);
    else {
        if(lcs(ia+1, ib) > lcs(ia, ib+1))
            ret = lcs(ia+1, ib);
        else
            ret = lcs(ia, ib+1);
    }

    return dp[ia][ib] = ret;
}

void print_lcs(int ia, int ib)
{
#ifdef VISOK
    if(vis[ia][ib]) return;
#endif // VISOK

    if(ia == len_a || ib == len_b) {
        cout << nxt << '\n';
        return;
    }

    if(a[ia] == b[ib]) {
        nxt.push_back(a[ia]);
        print_lcs(ia+1, ib+1);
        nxt.pop_back();
    }
    else {
        if(dp[ia+1][ib] > dp[ia][ib+1]) print_lcs(ia+1, ib);
        else if(dp[ia+1][ib] < dp[ia][ib+1])print_lcs(ia, ib+1);
        else {
            print_lcs(ia+1, ib);
            print_lcs(ia, ib+1);
        }
    }

#ifdef VISOK
    vis[ia][ib] = true;
#endif // VISOK
}

int main()
{
    a = /*"hello";*/ "HELLOM";
    b = /*"loxhe";*/ "HOMLLD";

    len_a = a.length();
    len_b = b.length();

    fill_n(&dp[0][0], 100, -1);

    cout << lcs(0, 0) << '\n';

    print_lcs(0, 0);

    return 0;
}

#include <iostream>
using namespace std;

const int MAXLEN = 1000+3;

int table[MAXLEN][MAXLEN];

int lcs_len(string a, string b)
{
    int m = a.length(), n = b.length();

    for(int i = 0; i <= m; ++i) table[i][n] = 0;
    for(int i = 0; i <= n; ++i) table[m][i] = 0;

    for(int i = m-1; i >= 0; --i) {
        for(int j = n-1; j >= 0; --j) {
            if(a[i] == b[j]) table[i][j] = 1 + table[i+1][j+1];
            else table[i][j] = max(table[i+1][j], table[i][j+1]);
        }
    }

    return table[0][0];
}

string get_sol(string a, string b)
{
    string sol;

    int m = a.length(), n = b.length();

    int i = 0;
    int j = 0;

    while(i < m && j < n) {
        if(a[i] == b[j]) {
            sol.push_back(a[i]);
            ++i, ++j;
        }
        else if(table[i+1][j] > table[i][j+1]) ++i;
        else ++j;
    }

    return sol;
}

int main()
{
    string str1, str2;
    //cin >> str1 >> str2;
    str1 = "akbucmdn";
    str2 = "ayybcd";

    cout << "Length of LCS : " << lcs_len(str1, str2) << '\n';

    string sol = get_sol(str1, str2);
    cout << sol << '\n';

    return 0;
}

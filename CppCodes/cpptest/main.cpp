// ==================================================
// Problem  :   1021 - Banknotes and Coins
// Run time :   0.000 sec.
// Language :   C++11
// ==================================================

#include <iostream>
#include <vector>
using namespace std;

int main()
{
    ios::sync_with_stdio(false);

    //freopen("in.txt", "r", stdin);

    int t;
    cin >> t;

    for(int tc = 1; tc <= t; ++tc) {
        vector<string> V;
        string s;
        int val, max_val = 0;

        for(int i = 0; i < 10; ++i) {
            cin >> s >> val;
            if(val > max_val) {
                V.clear();
                V.push_back(s);
                max_val = val;
            }
            else if(val == max_val) {
                V.push_back(s);
            }
        }

        cout << "Case #" << tc << ":\n";

        for(auto &url : V) cout << url << "\n";
    }

    return 0;
}

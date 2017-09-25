#include <cstdio>
#include <map>
#include <cstdlib>
using namespace std;

#define     ff                  first
#define     ss                  second

typedef     pair<int,int>       ii;

const char NOMATCH = -1;
const char playerSymbol = 'O';
const char compSymbol = 'X';

char grid[3][3];

char &a = grid[0][0], &b = grid[0][1], &c = grid[0][2];
char &d = grid[1][0], &e = grid[1][1], &f = grid[1][2];
char &g = grid[2][0], &h = grid[2][1], &i = grid[2][2];

char A, B, C, D, E, F, G, H, I;
map<char, ii> mp;

enum line {noLine, upLine, downLine, leftLine, rightLine, midVerticalLine, midHorizontalLine, cross1Line, cross2Line};

void init()
{
    //A = 'a', B = 'b', C = 'c', D = 'd', E = 'e', F = 'f', G = 'g', H = 'h', I = 'i';
    //A = 'A', B = 'B', C = 'C', D = 'D', E = 'E', F = 'F', G = 'G', H = 'H', I = 'I';
    A = '1', B = '2', C = '3', D = '4', E = '5', F = '6', G = '7', H = '8', I = '9';

    mp[A] = ii(0, 0), mp[B] = ii(0, 1), mp[C] = ii(0, 2);
    mp[D] = ii(1, 0), mp[E] = ii(1, 1), mp[F] = ii(1, 2);
    mp[G] = ii(2, 0), mp[H] = ii(2, 1), mp[I] = ii(2, 2);
}

void fill_grid(char ch)
{
    for(int i = 0; i < 3; ++i)
        for(int j = 0; j < 3; ++j)
            grid[i][j] = ch;
}

void print_grid()
{
    printf("-------------\t\t\t-------------\n");

    printf("| %c | %c | %c |\t\t\t| %c | %c | %c |\n", grid[0][0], grid[0][1], grid[0][2], A, B, C);
    printf("-------------\t\t\t-------------\n");

    printf("| %c | %c | %c |\t\t\t| %c | %c | %c |\n", grid[1][0], grid[1][1], grid[1][2], D, E, F);
    printf("-------------\t\t\t-------------\n");

    printf("| %c | %c | %c |\t\t\t| %c | %c | %c |\n", grid[2][0], grid[2][1], grid[2][2], G, H, I);
    printf("-------------\t\t\t-------------\n");
}

char check_up_line()
{
    if(grid[0][0] == grid[0][1] && grid[0][0] == grid[0][2]) return grid[0][0];
    return NOMATCH;
}

char check_down_line()
{
    if(grid[2][0] == grid[2][1] && grid[2][0] == grid[2][2]) return grid[2][0];
    return NOMATCH;
}

char check_left_line()
{
    if(grid[0][0] == grid[1][0] && grid[0][0] == grid[2][0]) return grid[0][0];
    return NOMATCH;
}

char check_right_line()
{
    if(grid[0][2] == grid[1][2] && grid[0][2] == grid[2][2]) return grid[0][2];
    return NOMATCH;
}

char check_mid_vertical_line()
{
    if(grid[0][1] == grid[1][1] && grid[0][1] == grid[2][1]) return grid[0][1];
    return NOMATCH;
}

char check_mid_horizontal_line()
{
    if(grid[1][0] == grid[1][1] && grid[1][0] == grid[1][2]) return grid[1][0];
    return NOMATCH;
}

char check_cross1_line()
{
    if(grid[0][0] == grid[1][1] && grid[0][0] == grid[2][2]) return grid[0][0];
    return NOMATCH;
}

char check_cross2_line()
{
    if(grid[0][2] == grid[1][1] && grid[0][2] == grid[2][0]) return grid[0][2];
    return NOMATCH;
}

line which_line_match()
{
    if(check_up_line() == grid[0][0] && grid[0][0] != ' ') return upLine;
    if(check_down_line() == grid[2][0] && grid[2][0] != ' ') return downLine;
    if(check_left_line() == grid[0][0] && grid[0][0] != ' ') return leftLine;
    if(check_right_line() == grid[0][2] && grid[0][2] != ' ') return rightLine;
    if(check_mid_vertical_line() == grid[0][1] && grid[0][1] != ' ') return midVerticalLine;
    if(check_mid_horizontal_line() == grid[1][0] && grid[1][0] != ' ') return midHorizontalLine;
    if(check_cross1_line() == grid[0][0] && grid[0][0] != ' ') return cross1Line;
    if(check_cross2_line() == grid[0][2] && grid[0][2] != ' ') return cross2Line;
    return noLine;
}

void get_valid_turn(int &r, int &c)
{
    char ch[2];

    while(true) {
        printf("Now your turn: ");
        scanf("%s", ch);

        r = mp[ch[0]].ff, c = mp[ch[0]].ss;

        if(ch[0] < A || I < ch[0] || grid[r][c] != ' ') {
            printf("Wrong input !\n");
        }
        else break;
    }
}

bool yes_or_no()
{
    char ch[2];

    printf("Press 'y' for YES, 'n' for NO : ");
    scanf("%s", ch);

    return (ch[0] != 'n' && ch[0] != 'N');
}

bool isSafeTurn(int r, int c, char symbol)
{
    grid[r][c] = symbol;
    if(which_line_match() != noLine) {
        grid[r][c] = ' ';
        return true;
    }

    char nowSymbol = ((symbol == playerSymbol)? compSymbol : playerSymbol);

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 3; ++j) {
            if(grid[i][j] == ' ') {
                if(isSafeTurn(i, j, nowSymbol)) {
                    grid[r][c] = ' ';
                    return false;
                }
            }
        }
    }

    grid[r][c] = ' ';
    return true;
}

bool isImmediateWinningTurn(int r, int c, char symbol)
{
    grid[r][c] = symbol;
    if(which_line_match() != noLine) {
        grid[r][c] = ' ';
        return true;
    }

    grid[r][c] = ' ';
    return false;
}

bool areBothBlank(char x, char y)
{
    return (x == ' ' && y == ' ');
}

bool lastly_any_scope()
{
    if(a == compSymbol) {
        if(areBothBlank(b, c)) { b = compSymbol; return true; }
        if(areBothBlank(d, g)) { d = compSymbol; return true; }
        if(areBothBlank(e, i)) { e = compSymbol; return true; }
    }
    if(b == compSymbol) {
        if(areBothBlank(a, c)) { a = compSymbol; return true; }
        if(areBothBlank(e, h)) { e = compSymbol; return true; }
    }
    if(c == compSymbol) {
        if(areBothBlank(a, b)) { a = compSymbol; return true; }
        if(areBothBlank(f, i)) { f = compSymbol; return true; }
        if(areBothBlank(e, g)) { e = compSymbol; return true; }
    }
    if(d == compSymbol) {
        if(areBothBlank(a, g)) { a = compSymbol; return true; }
        if(areBothBlank(e, f)) { e = compSymbol; return true; }
    }
    if(e == compSymbol) {
        if(areBothBlank(a, i)) { a = compSymbol; return true; }
        if(areBothBlank(c, g)) { c = compSymbol; return true; }
        if(areBothBlank(b, h)) { b = compSymbol; return true; }
        if(areBothBlank(d, f)) { d = compSymbol; return true; }
    }
    if(f == compSymbol) {
        if(areBothBlank(c, i)) { c = compSymbol; return true; }
        if(areBothBlank(d, e)) { d = compSymbol; return true; }
    }
    if(g == compSymbol) {
        if(areBothBlank(a, d)) { a = compSymbol; return true; }
        if(areBothBlank(c, e)) { c = compSymbol; return true; }
        if(areBothBlank(h, i)) { h = compSymbol; return true; }
    }
    if(h == compSymbol) {
        if(areBothBlank(b, e)) { b = compSymbol; return true; }
        if(areBothBlank(g, i)) { g = compSymbol; return true; }
    }
    if(i == compSymbol) {
        if(areBothBlank(c, f)) { c = compSymbol; return true; }
        if(areBothBlank(a, e)) { a = compSymbol; return true; }
        if(areBothBlank(g, h)) { g = compSymbol; return true; }
    }

    return false;
}

void comp_turn_inc()
{
    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 3; ++j) {
            if(grid[i][j] == ' ') {
                if(isImmediateWinningTurn(i, j, compSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 3; ++j) {
            if(grid[i][j] == ' ') {
                if(isImmediateWinningTurn(i, j, playerSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 3; ++j) {
            if(grid[i][j] == ' ') {
                if(isSafeTurn(i, j, compSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    if(grid[1][1] == ' ') {
        grid[1][1] = compSymbol;
        return;
    }

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 3; ++j) {
            if(grid[i][j] == ' ') {
                if(isSafeTurn(i, j, playerSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    if(lastly_any_scope()) return;

    for(int i = 0; i < 3; ++i) {
        for(int j = 0; j < 3; ++j) {
            if(grid[i][j] == ' ') {
                grid[i][j] = compSymbol;
                return;
            }
        }
    }
}

void comp_turn_dec()
{
    for(int i = 2; i >= 0; --i) {
        for(int j = 2; j >= 0; --j) {
            if(grid[i][j] == ' ') {
                if(isImmediateWinningTurn(i, j, compSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    for(int i = 2; i >= 0; --i) {
        for(int j = 2; j >= 0; --j) {
            if(grid[i][j] == ' ') {
                if(isImmediateWinningTurn(i, j, playerSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    for(int i = 2; i >= 0; --i) {
        for(int j = 2; j >= 0; --j) {
            if(grid[i][j] == ' ') {
                if(isSafeTurn(i, j, compSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    if(grid[1][1] == ' ') {
        grid[1][1] = compSymbol;
        return;
    }

    for(int i = 2; i >= 0; --i) {
        for(int j = 2; j >= 0; --j) {
            if(grid[i][j] == ' ') {
                if(isSafeTurn(i, j, playerSymbol)) {
                    grid[i][j] = compSymbol;
                    return;
                }
            }
        }
    }

    if(lastly_any_scope()) return;

    for(int i = 2; i >= 0; --i) {
        for(int j = 2; j >= 0; --j) {
            if(grid[i][j] == ' ') {
                grid[i][j] = compSymbol;
                return;
            }
        }
    }
}

void comp_turn(int x)
{
    if(x == 0) comp_turn_inc();
    else comp_turn_dec();
}

int main()
{
    init();

    while(true) {
        printf("\nComp will turn first ?\n");
        bool whoTurnsFirst = yes_or_no();

        fill_grid(' ');
        int turnCnt = 0;

        if(whoTurnsFirst) {
            printf("\nComp turns:\n");
            grid[1][1] = compSymbol;
            ++turnCnt;
        }

        print_grid();

        while(true) {
            int r, c;
            printf("\n");
            get_valid_turn(r, c);
            grid[r][c] = playerSymbol;
            print_grid();
            ++turnCnt;

            if(which_line_match() != noLine) {
                printf("\nCongratulations ! You are winner !!!\n");
                break;
            }

            if(turnCnt == 9) {
                printf("\nNobody won !!!\n");
                break;
            }

            printf("\nComp turns:\n");
            bool incOrDec = rand() & 1;
            comp_turn(incOrDec);
            print_grid();
            ++turnCnt;

            if(which_line_match() != noLine) {
                printf("\nComp is winner !!!\n");
                break;
            }

            if(turnCnt == 9) {
                printf("\nNobody won !!!\n");
                break;
            }
        }

        printf("\n=============================================\n");
        printf("\nWanna play again ?\n");

        if(!yes_or_no()) {
            puts("\n- - - - - Thank You - - - - -");
            break;
        }
    }

    return 0;
}

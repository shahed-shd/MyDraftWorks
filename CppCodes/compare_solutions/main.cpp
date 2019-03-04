#include <cstdio>
#include <string>
#include <utility>
using namespace std;

int CMP_TOT = 1;
string GEN_FILE_NAME = "gen.cpp";
string SOLUTION_A_FILE_NAME = "sol_a.cpp";
string SOLUTION_B_FILE_NAME = "sol_b.cpp";


pair<string, string> split_file_name_ext(const string &file_name)
{
    size_t dot_pos = file_name.rfind('.');
    string name, ext;

    if(dot_pos != string::npos) {
        name = file_name.substr(0, dot_pos);
        ext = file_name.substr(dot_pos+1);
    }
    else {
        name = file_name;
    }

    return make_pair(name, ext);
}

int build_executable(string cpp_file_name, string executable_file_name="")
{
    if(executable_file_name.empty()) {
        executable_file_name = split_file_name_ext(cpp_file_name).first;
    }
    string cmd = "g++ -std=c++14 -Wall " + cpp_file_name + " -o " + executable_file_name;
    return system(cmd.c_str());
}

int main()
{
    // Remove old files if exists.
    system("rm -f gen in.txt sol_a out_a.txt sol_b out_b.txt");

    // Run sol_a.cpp and get executable file.
    executable_a_file_name = split_file_name_ext(SOLUTION_A_FILE_NAME).first;
    build_executable(SOLUTION_A_FILE_NAME, executable_a_file_name);

    // Run sol_b.cpp and get executable file.
    executable_b_file_name = split_file_name_ext(SOLUTION_B_FILE_NAME).first;
    build_executable(SOLUTION_B_FILE_NAME, executable_b_file_name);

    for(int cmp_cnt = 1; cmp_cnt <= CMP_TOT; ++cmp_cnt) {
        // Run gen.cpp and generato in.txt input file.
        string executable_gen_file_name = split_file_name_ext(GEN_FILE_NAME).first;
        build_executable(GEN_FILE_NAME, executable_gen_file_name);
        string cmd_string = "./" + executable_gen_file_name + " > in.txt";
        system(cmd_string.c_str());

        // Get output from solution A in out_a.txt
        cmd_string = "./" + executable_a_file_name + " < in.txt > out_a.txt";
        system(cmd_string.c_str());

        // Get output from solution B in out_b.txt
        cmd_string = "./" + executable_b_file_name + " < in.txt > out_b.txt";
        system(cmd_string.c_str());

        // diff
        int diff_ret = system("diff out_a.txt out_b.txt");

        // Output
        printf("cmp %d: ", cmp_cnt);
        if(diff_ret == 0) {
            printf("OK\n");
        }
        else {
            printf("Mismatch found ! ");
            printf("diff_ret: %d\n", diff_ret);
            break;
        }
    }

    return 0;
}
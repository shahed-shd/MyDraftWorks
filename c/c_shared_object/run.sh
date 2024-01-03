function clean_all() {
    rm *.so
    rm main
}

function compile_all() {
    gcc -shared -o libsharedutils.so impladd.c implmultiply.c
    gcc -L. -lsharedutils -o main main.c 
}

clean_all
compile_all
./main

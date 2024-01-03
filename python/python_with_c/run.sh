rm *.so
gcc -shared -o libsharedutils.so impladd.c implmultiply.c
python main.py
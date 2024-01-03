function clear_all() {
    rm *.so
    rm *.class
}


function compile_all() {
    gcc -shared -o libsharedutils.so impladd.c implmultiply.c
    javac --class-path jna-5.14.0.jar:. Main.java
}

clear_all
compile_all
java --class-path jna-5.14.0.jar:. Main

# If need to specify library path
# LD_LIBRARY_PATH=.
# java --class-path jna-5.14.0.jar:. -Djava.library.path=. Main

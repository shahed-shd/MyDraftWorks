function clear_all() {
    rm *.so
    rm *.class
}


function compile_all() {
    JAVA_HOME=$(asdf where java)
    
    # For linux
    # gcc -I${JAVA_HOME}/include -I${JAVA_HOME}/include/linux -shared -o libadd.so add.c
    
    # For Mac
    gcc -I${JAVA_HOME}/include -I${JAVA_HOME}/include/darwin -shared -o libsharedutils.so impladd.c implmultiply.c
    
    javac Main.java
}

clear_all
compile_all
java Main

# If need to specify library path
# java -Djava.library.path=. Main 
# LD_LIBRARY_PATH=.
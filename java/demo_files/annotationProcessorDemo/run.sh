function clear_all() {
    find . -name "*.class" -exec rm {} \;
    rm -r build/classes/*
    rm -r build/generated/*
}

function compile_all() {
    # Compile processor
    javac -d build/classes src/com/example/processor/BuilderProcessor.java

    # Compile annotation
    javac -d build/classes src/com/example/annotation/BuilderProperty.java

    # Create jar including the processor and use it as processor
    # jar --verbose --create --file build/libs/builderProcessor.jar -C build/classes com/example/processor/BuilderProcessor.class
    # javac --class-path build/classes --processor-path build/libs/* -processor com.example.processor.BuilderProcessor -d build/classes src/com/example/Person.java
    
    # Alternatively, without creating jar.
    # Here, `--processor-path` can be ommited because class-path will be used to search for processor then.
    # Also place the generated java file in a specific directory
    javac --class-path build/classes --processor-path build/classes -processor com.example.processor.BuilderProcessor -d build/classes -s build/generated src/com/example/Person.java
    
    # Compile Main.java
    javac --class-path build/classes -d build/classes src/com/example/Main.java
}

clear_all
compile_all
java --class-path build/classes com.example.Main



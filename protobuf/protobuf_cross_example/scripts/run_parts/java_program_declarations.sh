
JAVA_DEPENDENCIES_DIR_FROM_JAVA_PROGRM_DIR=deps
JAVA_BUILD_DIR_FROM_JAVA_PROGRM_DIR=build

function genJava() {
    # Linux: apt install -y protobuf-compiler
    # Mac: brew install protobuf
    protoc --proto_path="$PROTO_FILES_PATH_FROM_ROOT_DIR" --java_out=./java/src $(find "$PROTO_FILES_PATH_FROM_ROOT_DIR" -name "*.proto")
}

function rmGenJava() {
    if [ -d "java/src/protogen" ] ; then
        log "Foung protogen for java program, removing."
        rm -rf java/src/protogen
    else
        log "No protogen for java program."
    fi
}

function check_and_download_dependency() {
    file="$1"
    download_url="$2"

    if [ -e "$JAVA_DEPENDENCIES_DIR_FROM_JAVA_PROGRM_DIR/$file" ] ; then
        log "Dependency $file found downloaded"
    else
        log "Dependency $file downloading..."
        wget --directory-prefix="$JAVA_DEPENDENCIES_DIR_FROM_JAVA_PROGRM_DIR" "$download_url"
    fi
}

function compileJava() {
    cd java
    check_and_download_dependency 'protobuf-java-4.32.0.jar' 'https://repo1.maven.org/maven2/com/google/protobuf/protobuf-java/4.32.0/protobuf-java-4.32.0.jar'
    rm -r "$JAVA_BUILD_DIR_FROM_JAVA_PROGRM_DIR"
    javac -cp "src:$JAVA_DEPENDENCIES_DIR_FROM_JAVA_PROGRM_DIR/*" -d "$JAVA_BUILD_DIR_FROM_JAVA_PROGRM_DIR" src/Main.java
    cd ..
}

function runJava() {
    command=$1
    cd java
    java -cp "$JAVA_BUILD_DIR_FROM_JAVA_PROGRM_DIR:$JAVA_DEPENDENCIES_DIR_FROM_JAVA_PROGRM_DIR/*" Main "$command" "../$SERIALIZED_FILE_PATH_FROM_ROOT_DIR"
    cd ..
}

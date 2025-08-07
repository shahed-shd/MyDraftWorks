
function genPython() {
    # Linux: apt install -y protobuf-compiler
    # Mac: brew install protobuf

    # With betterproto
    genPythonWithBetterproto

    # Or, alternatively,
    # ToDo: Need some fix to generate without betterproto
    # protoc --proto_path="$PROTO_FILES_PATH_FROM_ROOT_DIR" --python_out=./python/src $(find "$PROTO_FILES_PATH_FROM_ROOT_DIR" -name "*.proto")
}

function genPythonWithBetterproto() {
    # Needs `betterproto` installed.
    # pip install "betterproto[compiler]"
    protoc --proto_path="$PROTO_FILES_PATH_FROM_ROOT_DIR" --python_betterproto_opt=typing.310 --python_betterproto_out=./python/src $(find "$PROTO_FILES_PATH_FROM_ROOT_DIR" -name "*.proto")
        # --proto_path : tells protoc where to start resolving imports like `import "address.proto";`

    # Fix import statements
    if [[ "$OSTYPE" == "darwin"* ]]; then   # Mac
        sed -i '' 's/from .protogen import enums/from protogen import enums/' python/src/protogen/models.py
    else    # Linux
        sed -i 's/from .protogen import enums/from protogen import enums/' python/src/protogen/models.py
    fi
}

function rmGenPython() {
    if [ -d "python/src/protogen" ] ; then
        log "Foung protogen for python program, removing."
        rm -rf python/src/protogen
    else
        log "No protogen for python program."
    fi
}

function runPython() {
    command=$1
    cd python

    # Use virtual environment if needed.
    # pip install protobuf
    python src/main.py "$command" "../$SERIALIZED_FILE_PATH_FROM_ROOT_DIR"
    
    cd ..
}

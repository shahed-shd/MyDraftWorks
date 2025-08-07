PROTO_FILES_PATH_FROM_ROOT_DIR=protos
SERIALIZED_FILE_PATH_FROM_ROOT_DIR=serialized.bin

function log() {
    local message="$1"
    printf "$( date +"%Y-%m-%dT%H:%M:%S%z" ) INFO: $message\n"
}

function divideOutput() {
    echo

    for (( i = 0; i < 80; i++ )); do
        echo -n '#'
    done

    echo
    echo

}

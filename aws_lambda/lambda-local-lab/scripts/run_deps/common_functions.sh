logSection() {
    printf "\n\n============================== %s ==============================\n" "${1}"
}

logInfo() {
    printf "\n[INFO] %s\n" "${1}"
}

# Set AWS CLI to use LocalStack endpoint
awslocal() {
    aws --endpoint-url=http://localhost:4566 "$@"
}
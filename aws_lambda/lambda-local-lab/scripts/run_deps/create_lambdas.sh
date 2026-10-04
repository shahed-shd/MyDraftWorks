logSection "Creating Lambdas"

function create_lambda_if_not_exists() {
    local function_name="$1"
    local runtime="$2"
    local handler="$3"
    local role_arn="$4"
    local zip_file_path="$5"

    if ! awslocal lambda get-function --function-name "$function_name" >/dev/null 2>&1; then
        awslocal \
            lambda create-function \
            --function-name "$function_name" \
            --runtime "$runtime" \
            --handler "$handler" \
            --role "$role_arn" \
            --zip-file "fileb://$zip_file_path"
    else
        logInfo "Lambda $function_name already exists. Skipping creation."
    fi
}

# Create the Java Lambda
logInfo "Creating lambda ${JAVA_LAMBDA}"
create_lambda_if_not_exists "${JAVA_LAMBDA}" "java21" "example.HelloHandler" "${ROLE_ARN}" "lambda-java.zip"

logInfo "Creating lambda ${JAVA_WORKER_LAMBDA}"
create_lambda_if_not_exists "${JAVA_WORKER_LAMBDA}" "java21" "example.WorkerHandler" "${ROLE_ARN}" "lambda-java.zip"

# Create the Python Lambda
logInfo "Creating lambda ${PYTHON_LAMBDA}"
create_lambda_if_not_exists "${PYTHON_LAMBDA}" "python3.12" "hello_handler.handler" "${ROLE_ARN}" "lambda-python-hello.zip"

logInfo "Creating lambda ${PYTHON_WORKER_LAMBDA}"
create_lambda_if_not_exists "${PYTHON_WORKER_LAMBDA}" "python3.12" "worker_handler.handler" "${ROLE_ARN}" "lambda-python-worker.zip"

# List lambdas to verify creation
logInfo "Listing all lambdas to verify creation"
# awslocal lambda list-functions | jq '.Functions[] | {FunctionName, Runtime, Handler, Role}'
awslocal lambda list-functions --query 'Functions[*].[FunctionName, Runtime, Handler, Role]'
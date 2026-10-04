logSection "CLI Invocation"

input_dir_path_from_root="scripts/inputs"
output_dir_path_from_root="scripts/outputs"

# Invoke the Java Lambda
logInfo "Invoking Java Lambda ${JAVA_LAMBDA}"

awslocal lambda invoke \
    --function-name "${JAVA_LAMBDA}" \
    --invocation-type RequestResponse \
    --cli-binary-format raw-in-base64-out \
    --payload "file://${input_dir_path_from_root}/payload.json" \
    "${output_dir_path_from_root}/${JAVA_LAMBDA}_response.json"


logInfo "Invoking Java Lambda ${JAVA_WORKER_LAMBDA}"

awslocal lambda invoke \
    --function-name "${JAVA_WORKER_LAMBDA}" \
    --invocation-type Event \
    --cli-binary-format raw-in-base64-out \
    --payload "file://${input_dir_path_from_root}/payload.json" \
    "${output_dir_path_from_root}/${JAVA_WORKER_LAMBDA}_response.json"


# Invoke the Python Lambda
logInfo "Invoking Python Lambda ${PYTHON_LAMBDA}"

awslocal lambda invoke \
    --function-name "${PYTHON_LAMBDA}" \
    --invocation-type RequestResponse \
    --cli-binary-format raw-in-base64-out \
    --payload file://${input_dir_path_from_root}/payload.json \
    "${output_dir_path_from_root}/${PYTHON_LAMBDA}_response.json"


logInfo "Invoking Python Lambda ${PYTHON_WORKER_LAMBDA}"

awslocal lambda invoke \
    --function-name "${PYTHON_WORKER_LAMBDA}" \
    --invocation-type Event \
    --cli-binary-format raw-in-base64-out \
    --payload file://${input_dir_path_from_root}/payload.json \
    "${output_dir_path_from_root}/${PYTHON_WORKER_LAMBDA}_response.json"

logInfo

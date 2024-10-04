curl -L --verbose 'http://127.0.0.1:8000/sample-any?a=x&b=y'


# curl -L --verbose http://127.0.0.1:8000/sample \
#     --json '{
#         "outerKey1": "outerValue1",
#         "outerKey2": {
#             "nestedKey1": "nestedValue1",
#             "nestedKey2": "nestedValue2"
#         }
#     }'


# curl -L --verbose http://127.0.0.1:8000/sample-any \
#     --json '{
#         "outerKey1": "outerValue1",
#         "outerKey2": {
#             "nestedKey1": "nestedValue1",
#             "nestedKey2": "nestedValue2"
#         }
#     }'

# curl -X PUT -L --verbose http://127.0.0.1:8000/sample-any \
# --json '{
#     "outerKey1": "outerValue1",
#     "outerKey2": {
#         "nestedKey1": "nestedValue1",
#         "nestedKey2": "nestedValue2"
#     }
# }'
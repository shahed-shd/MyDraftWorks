logSection "Creating IAM Role for Lambda functions"

role_name="lambda-lab-role"

if ! awslocal iam get-role --role-name "$role_name" >/dev/null 2>&1; then
  logInfo "Role does not exist. Creating role..."

  awslocal iam create-role \
    --role-name "$role_name" \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }]
    }'
else
  logInfo "Role $role_name already exists. Skipping."
fi
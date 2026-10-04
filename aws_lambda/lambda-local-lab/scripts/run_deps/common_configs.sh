#!/usr/bin/env bash

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=ap-southeast-1
export AWS_PAGER=""

export LOCALSTACK_URL=http://localhost:4566

export ACCOUNT_ID=000000000000
export REGION=ap-southeast-1

export JAVA_LAMBDA=java-hello
export PYTHON_LAMBDA=python-hello

export JAVA_WORKER_LAMBDA=java-worker
export PYTHON_WORKER_LAMBDA=python-worker

export ROLE_ARN=arn:aws:iam::${ACCOUNT_ID}:role/lambda-lab-role

export JAVA_LAMBDA_ARN=arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${JAVA_LAMBDA}
export PYTHON_LAMBDA_ARN=arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${PYTHON_LAMBDA}

export JAVA_WORKER_ARN=arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${JAVA_WORKER_LAMBDA}
export PYTHON_WORKER_ARN=arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${PYTHON_WORKER_LAMBDA}


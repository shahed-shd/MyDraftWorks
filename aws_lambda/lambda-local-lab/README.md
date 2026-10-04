# AWS Lambda Local Development Lab

A hands-on local development and learning environment for **AWS Lambda** using:

* [LocalStack](https://localstack.cloud/)
* Docker Compose
* Java 21 Lambda
* Python 3.12 Lambda
* AWS CLI
* Spring Boot WebFlux
* FastAPI
* EventBridge scheduled rules

The purpose of this project is to demonstrate how Lambda works, how it can be invoked, how scheduled triggers work, how synchronous and asynchronous invocation differ, and how an application can invoke Lambda functions.

> **Note:** This project is intended for local learning and integration testing. LocalStack emulates AWS services, but it is not identical to real AWS.

---

## Architecture

The local environment contains:

```text
                              ┌────────────────────────────┐
                              │         LocalStack         │
                              │                            │
                              │  ┌──────────────────────┐  │
                              │  │    Java Lambda       │  │
                              │  │    java-hello        │  │
                              │  └──────────────────────┘  │
                              │                            │
                              │  ┌──────────────────────┐  │
                              │  │    Java Worker       │  │
                              │  │    java-worker       │  │
                              │  └──────────────────────┘  │
                              │                            │
                              │  ┌──────────────────────┐  │
                              │  │   Python Lambda      │  │
                              │  │   python-hello       │  │
                              │  └──────────────────────┘  │
                              │                            │
                              │  ┌──────────────────────┐  │
                              │  │   Python Worker      │  │
                              │  │   python-worker      │  │
                              │  └──────────────────────┘  │
                              │                            │
                              │  ┌──────────────────────┐  │
                              │  │     EventBridge      │  │
                              │  │    rate / cron rules │  │
                              │  └──────────────────────┘  │
                              │                            │
                              └────────────────────────────┘
```

Applications can invoke Lambda through the AWS SDK:

```text
┌──────────────────┐
│ Spring Boot      │
│ WebFlux          │
└────────┬─────────┘
         │ AWS SDK
         ▼
┌────────────────────────────┐
│       LocalStack           │
│                            │
│       AWS Lambda           │
└────────────────────────────┘


┌──────────────────┐
│ FastAPI          │
└────────┬─────────┘
         │ boto3
         ▼
┌────────────────────────────┐
│       LocalStack           │
│                            │
│       AWS Lambda           │
└────────────────────────────┘
```

Scheduled invocation:

```text
                 EventBridge
                      │
            ┌─────────┴─────────┐
            │                   │
         rate(...)           cron(...)
            │                   │
            └─────────┬─────────┘
                      ▼
                   Lambda
```

---

# What This Project Demonstrates

This project covers:

1. Creating a Java Lambda.
2. Creating a Python Lambda.
3. Invoking Lambda from the AWS CLI.
4. Invoking Lambda synchronously.
5. Invoking Lambda asynchronously.
6. Receiving a Lambda return value from the CLI.
7. Invoking Lambda from a Spring Boot WebFlux application.
8. Invoking Lambda from a FastAPI application.
9. Receiving the Lambda return value from applications.
10. EventBridge `rate(...)` scheduled invocation.
11. EventBridge `cron(...)` scheduled invocation.
12. Minimal EventBridge event triggering.
13. Lambda logging.
14. Lambda exception handling.
15. Background processing using asynchronous Lambda invocation.
16. Understanding why starting a background thread inside Lambda is not a reliable architecture.
17. Understanding the difference between Lambda invocation success and Lambda function success.

---

# Important Lambda Concepts

## Synchronous invocation

The caller waits for Lambda to finish.

```text
Client
   │
   │ Invoke
   ▼
Lambda
   │
   │ execute
   ▼
Result
   │
   ▼
Client
```

AWS CLI:

```bash
aws lambda invoke \
    --function-name java-hello \
    --invocation-type RequestResponse \
    ...
```

The Lambda return value is available to the caller.

---

## Asynchronous invocation

The caller submits the event and receives an immediate acknowledgement.

```text
Client
   │
   │ Invoke
   ▼
Lambda service
   │
   ├──────────────► 202
   │
   ▼
Lambda execution
```

AWS CLI:

```bash
aws lambda invoke \
    --function-name java-worker \
    --invocation-type Event \
    ...
```

The caller does **not** receive the Lambda's eventual return value.

---

# Background Processing

If a client needs:

```text
immediate response
+
background processing
```

do not rely on:

```java
new Thread(() -> {
    doSomething();
}).start();

return response;
```

inside Lambda.

A better architecture is:

```text
Client
  │
  ▼
Starter Lambda
  │
  ├──────────────► immediate response
  │
  └── async ─────► Worker Lambda
                         │
                         ▼
                    background task
                         │
                         ▼
                    persist result
```

For a production architecture, an SQS queue between the starter and worker is often preferable:

```text
Client
  │
  ▼
API / Lambda
  │
  ▼
SQS
  │
  ▼
Worker Lambda
  │
  ▼
Database / S3 / external service
```

SQS provides useful capabilities such as:

* buffering
* retry
* visibility timeout
* dead-letter queues
* batching
* decoupling
* backpressure

---

# Project Structure

```text
lambda-local-lab/
│
├── docker-compose.yml
├── Makefile
├── payload.json
│
├── scripts/
│   ├── common.sh
│   ├── deploy.sh
│   └── schedule.sh
│
├── lambdas/
│   │
│   ├── java/
│   │   ├── build.gradle
│   │   ├── settings.gradle
│   │   └── src/
│   │       └── main/
│   │           └── java/
│   │               └── example/
│   │                   ├── HelloHandler.java
│   │                   └── WorkerHandler.java
│   │
│   └── python/
│       ├── hello_handler.py
│       └── worker_handler.py
│
├── java-client/
│   ├── build.gradle
│   ├── settings.gradle
│   └── src/
│       └── main/
│           └── java/
│               └── example/
│                   └── LambdaClientApplication.java
│
└── python-client/
    ├── requirements.txt
    └── app/
        └── main.py
```

---

# Prerequisites

* Docker
* Docker Compose
* AWS CLI
* Java 21
* Gradle
* Python 3.12+

The project uses:
- AWS region: `ap-southeast-1`
- LocalStack: http://localhost:4566

Check `scripts/run.sh` for verifying the prerequisites.

---

# AWS CLI Configuration

LocalStack does not require real AWS credentials.

Configure dummy credentials:

```bash
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set region ap-southeast-1
aws configure set cli_binary_format raw-in-base64-out
```

---

# LocalStack Docker Configuration

Check `docker-compose.yml`.

The Docker socket is mounted because LocalStack executes Lambda functions using Docker-based Lambda execution environments.

Start the environment:

```bash
docker compose up -d
```
Refer to `run.sh` to see verification commands

---

# Environment Variables

Check `scripts/common_configs.sh`.

Make scripts executable:

```bash
chmod +x scripts/*.sh
```

---

# Java Lambda

Gradle configuration:
  - `lambdas/java/settings.gradle`
  - `lambdas/java/build.gradle`
 
Java Hello Lambda:
  - `lambdas/java/src/main/java/example/HelloHandler.java`.
  - Handler: `example.HelloHandler`

Java Worker Lambda:
  - `lambdas/java/src/main/java/example/WorkerHandler.java`.
  - Handler: `example.WorkerHandler`

Packaging:
  - Build with gradle, output will be a `.zip` file
  - Copy the zip file to root directory.
  - Check `run.sh` for packaging commands.
---

# Python Lambda

Python Hello Lambda:
  - `lambdas/python/hello_handler.py`.

Python Worker Lambda:
  - `lambdas/python/worker_handler.py`.

Packaging:
  - Create separate `.zip` files for the handlers and put them in root dir
  - Check `run.sh` for packaging commands.

---

# Create IAM Role

Create a local IAM role and get a role RRN like
`arn:aws:iam::000000000000:role/lambda-lab-role`.

Check `run.sh` for the commands.

---

# Create Java Lambda
 Create lambdas. Then list them to verify creation.

 Check `run.sh` for the commands.

---

# CLI Invocation

Invoke lambdas from CLI.

Invocation types:
  - `RequestResponse`:
    - For synchronous invocation
    - The caller waits until the Lambda execution completes.
  - `Event`:
    - For asynchronous invocation
    - The CLI receives an acknowledgement simlar to `{"StatusCode": 202}`
    - The actual worker result is not returned.

Check `run.sh` for the commands.

---

# 27. Lambda Return Value

A synchronous Lambda can return any JSON-compatible value.

Java:

```java
return Map.of(
        "success", true,
        "message", "Hello"
);
```

Python:

```python
return {
    "success": True,
    "message": "Hello"
}
```

The AWS SDK/CLI receives the serialized result.

For synchronous invocation:

```text
Lambda return value
        │
        ▼
Invoke API response
        │
        ▼
Caller
```

For asynchronous invocation:

```text
Lambda return value
        │
        X
        │
        └── not returned to caller
```

---

# 28. Spring Boot WebFlux Client

The Java client demonstrates how a normal Java application can invoke Lambda using AWS SDK for Java v2.

## `java-client/settings.gradle`

```groovy
rootProject.name = 'lambda-java-client'
```

## `java-client/build.gradle`

```groovy
plugins {
    id 'java'

    id 'org.springframework.boot' version '3.3.12'

    id 'io.spring.dependency-management' version '1.1.7'
}

group = 'example'
version = '1.0.0'

java {
    sourceCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {

    implementation 'org.springframework.boot:spring-boot-starter-webflux'

    implementation platform(
        'software.amazon.awssdk:bom:2.28.29'
    )

    implementation 'software.amazon.awssdk:lambda'
}

tasks.named('test') {
    useJUnitPlatform()
}
```

---

# 29. Java Application

`java-client/src/main/java/example/LambdaClientApplication.java`

```java
package example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.*;

import reactor.core.publisher.Mono;

import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.lambda.LambdaAsyncClient;
import software.amazon.awssdk.services.lambda.model.InvocationType;
import software.amazon.awssdk.services.lambda.model.InvokeRequest;

import java.net.URI;
import java.nio.charset.StandardCharsets;

@SpringBootApplication
@RestController
public class LambdaClientApplication {

    private final LambdaAsyncClient lambda;

    public LambdaClientApplication(
            LambdaAsyncClient lambda) {

        this.lambda = lambda;
    }

    public static void main(String[] args) {
        SpringApplication.run(
                LambdaClientApplication.class,
                args
        );
    }

    @Bean
    LambdaAsyncClient lambdaClient() {

        return LambdaAsyncClient.builder()
                .endpointOverride(
                        URI.create(
                                "http://localhost:4566"
                        )
                )
                .region(
                        Region.AP_SOUTHEAST_1
                )
                .build();
    }

    @PostMapping("/invoke/java")
    public Mono<String> invokeJava(
            @RequestBody String payload) {

        InvokeRequest request =
                InvokeRequest.builder()
                        .functionName(
                                "java-hello"
                        )
                        .invocationType(
                                InvocationType.REQUEST_RESPONSE
                        )
                        .payload(
                                SdkBytes.fromString(
                                        payload,
                                        StandardCharsets.UTF_8
                                )
                        )
                        .build();

        return Mono.fromFuture(
                lambda.invoke(request)
        ).map(response ->
                response.payload()
                        .asUtf8String()
        );
    }

    @PostMapping("/invoke/python")
    public Mono<String> invokePython(
            @RequestBody String payload) {

        InvokeRequest request =
                InvokeRequest.builder()
                        .functionName(
                                "python-hello"
                        )
                        .invocationType(
                                InvocationType.REQUEST_RESPONSE
                        )
                        .payload(
                                SdkBytes.fromString(
                                        payload,
                                        StandardCharsets.UTF_8
                                )
                        )
                        .build();

        return Mono.fromFuture(
                lambda.invoke(request)
        ).map(response ->
                response.payload()
                        .asUtf8String()
        );
    }

    @PostMapping("/invoke/background")
    public Mono<String> invokeBackground(
            @RequestBody String payload) {

        InvokeRequest request =
                InvokeRequest.builder()
                        .functionName(
                                "java-worker"
                        )
                        .invocationType(
                                InvocationType.EVENT
                        )
                        .payload(
                                SdkBytes.fromString(
                                        payload,
                                        StandardCharsets.UTF_8
                                )
                        )
                        .build();

        return Mono.fromFuture(
                lambda.invoke(request)
        ).map(response ->
                """
                {
                  "accepted": true,
                  "lambdaStatusCode": %d
                }
                """.formatted(
                        response.statusCode()
                )
        );
    }
}
```

---

# 30. Start the Java Client

```bash
cd java-client

gradle bootRun
```

The application runs on:

```text
http://localhost:8080
```

---

# 31. Java Application → Java Lambda

```bash
curl \
  -X POST \
  http://localhost:8080/invoke/java \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shahed"}'
```

The Java application waits for Lambda and returns its result.

Flow:

```text
HTTP client
    │
    ▼
Spring WebFlux
    │
    ▼
AWS SDK
    │
    ▼
LocalStack Lambda
    │
    ▼
Java Lambda
    │
    ▼
return value
    │
    ▼
Spring WebFlux
    │
    ▼
HTTP client
```

---

# 32. Java Application → Python Lambda

```bash
curl \
  -X POST \
  http://localhost:8080/invoke/python \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shahed"}'
```

The same Java application can invoke either Java or Python Lambda.

---

# 33. Java Application → Background Lambda

```bash
curl \
  -X POST \
  http://localhost:8080/invoke/background \
  -H 'Content-Type: application/json' \
  -d '{"job":"123"}'
```

The response is immediate:

```json
{
  "accepted": true,
  "lambdaStatusCode": 202
}
```

The worker continues independently.

---

# 34. FastAPI Client

`python-client/requirements.txt`:

```text
fastapi
uvicorn[standard]
boto3
```

Create a virtual environment:

```bash
cd python-client

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

---

# 35. FastAPI Application

`python-client/app/main.py`:

```python
import json
import os

import boto3

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


lambda_client = boto3.client(
    "lambda",

    endpoint_url=os.getenv(
        "LAMBDA_ENDPOINT",
        "http://localhost:4566"
    ),

    region_name="ap-southeast-1",

    aws_access_key_id="test",
    aws_secret_access_key="test",
)


class Payload(BaseModel):
    name: str


@app.post("/invoke/java")
def invoke_java(payload: Payload):

    response = lambda_client.invoke(
        FunctionName="java-hello",

        InvocationType="RequestResponse",

        Payload=json.dumps(
            payload.model_dump()
        ).encode(),
    )

    result = json.loads(
        response["Payload"].read()
    )

    return result


@app.post("/invoke/python")
def invoke_python(payload: Payload):

    response = lambda_client.invoke(
        FunctionName="python-hello",

        InvocationType="RequestResponse",

        Payload=json.dumps(
            payload.model_dump()
        ).encode(),
    )

    result = json.loads(
        response["Payload"].read()
    )

    return result


@app.post("/invoke/background")
def invoke_background(payload: Payload):

    response = lambda_client.invoke(
        FunctionName="python-worker",

        InvocationType="Event",

        Payload=json.dumps(
            payload.model_dump()
        ).encode(),
    )

    return {
        "accepted": True,
        "lambda_status_code": response["StatusCode"],
    }
```

---

# 36. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

FastAPI:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# 37. FastAPI → Java Lambda

```bash
curl \
  -X POST \
  http://localhost:8000/invoke/java \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shahed"}'
```

---

# 38. FastAPI → Python Lambda

```bash
curl \
  -X POST \
  http://localhost:8000/invoke/python \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shahed"}'
```

---

# 39. FastAPI → Background Lambda

```bash
curl \
  -X POST \
  http://localhost:8000/invoke/background \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shahed"}'
```

Response:

```json
{
  "accepted": true,
  "lambda_status_code": 202
}
```

---

# 40. EventBridge Scheduled Invocation

This project uses **EventBridge scheduled rules** for local scheduled execution.

Two types are demonstrated:

```text
rate(...)
cron(...)
```

---

# 41. `rate(...)` Schedule

Create a Java rule that runs every minute:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-rule \
  --name java-lambda-rate \
  --schedule-expression "rate(1 minute)" \
  --state ENABLED
```

The conceptual flow is:

```text
EventBridge
    │
    │ every 1 minute
    ▼
java-hello
```

---

# 42. EventBridge Permission

Allow EventBridge to invoke the Lambda:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda add-permission \
  --function-name java-hello \
  --statement-id eventbridge-java-rate \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn \
  arn:aws:events:ap-southeast-1:000000000000:rule/java-lambda-rate
```

---

# 43. Add Lambda as EventBridge Target

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-targets \
  --rule java-lambda-rate \
  --targets \
  "Id=java-lambda,Arn=arn:aws:lambda:ap-southeast-1:000000000000:function:java-hello"
```

---

# 44. Python `rate(...)` Schedule

Create:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-rule \
  --name python-lambda-rate \
  --schedule-expression "rate(1 minute)" \
  --state ENABLED
```

Permission:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda add-permission \
  --function-name python-hello \
  --statement-id eventbridge-python-rate \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn \
  arn:aws:events:ap-southeast-1:000000000000:rule/python-lambda-rate
```

Target:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-targets \
  --rule python-lambda-rate \
  --targets \
  "Id=python-lambda,Arn=arn:aws:lambda:ap-southeast-1:000000000000:function:python-hello"
```

---

# 45. `cron(...)` Schedule

AWS EventBridge cron expressions contain six fields:

```text
minute
hour
day-of-month
month
day-of-week
year
```

For example:

```text
cron(0 * * * ? *)
```

means:

```text
At minute 0 of every hour.
```

Create:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-rule \
  --name java-lambda-hourly \
  --schedule-expression "cron(0 * * * ? *)" \
  --state ENABLED
```

Permission:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda add-permission \
  --function-name java-hello \
  --statement-id eventbridge-java-cron \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn \
  arn:aws:events:ap-southeast-1:000000000000:rule/java-lambda-hourly
```

Target:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-targets \
  --rule java-lambda-hourly \
  --targets \
  "Id=java-lambda-cron,Arn=arn:aws:lambda:ap-southeast-1:000000000000:function:java-hello"
```

---

# 46. Minimal EventBridge Event Trigger

A scheduled rule is not the only way EventBridge can invoke Lambda.

Create an event-pattern rule:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-rule \
  --name minimal-java-event \
  --event-pattern '{
    "source": ["demo"]
  }'
```

Allow invocation:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda add-permission \
  --function-name java-hello \
  --statement-id eventbridge-java-event \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn \
  arn:aws:events:ap-southeast-1:000000000000:rule/minimal-java-event
```

Attach target:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-targets \
  --rule minimal-java-event \
  --targets \
  "Id=java-lambda,Arn=arn:aws:lambda:ap-southeast-1:000000000000:function:java-hello"
```

Publish an event:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events put-events \
  --entries '[
    {
      "Source": "demo",
      "DetailType": "DemoEvent",
      "Detail": "{\"message\":\"hello\"}"
    }
  ]'
```

Flow:

```text
put-events
    │
    ▼
EventBridge
    │
    │ source == demo
    ▼
java-hello
```

---

# 47. Schedule Script

The provided:

```text
scripts/schedule.sh
```

configures:

```text
java-lambda-rate
python-lambda-rate
java-lambda-cron
```

Run:

```bash
./scripts/schedule.sh
```

Verify rules:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events list-rules
```

---

# 48. Verify EventBridge Targets

For Java:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events list-targets-by-rule \
  --rule java-lambda-rate
```

For Python:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events list-targets-by-rule \
  --rule python-lambda-rate
```

---

# 49. "Execute After N Minutes"

There are two different concepts that should not be confused.

## Repeating schedule

```text
rate(5 minutes)
```

means:

```text
execute every 5 minutes
```

It does **not** mean:

```text
execute once 5 minutes from now
```

---

## One-time schedule

AWS EventBridge Scheduler supports:

```text
at(...)
```

for one-time execution.

For example:

```text
at(2026-10-04T10:30:00)
```

can represent a one-time schedule.

It also supports:

```text
rate(...)
cron(...)
```

for recurring schedules.

### LocalStack limitation

This project intentionally uses EventBridge scheduled rules for local execution.

LocalStack's Scheduler API and real AWS EventBridge Scheduler should not be assumed to have identical execution behavior in the local environment. In particular, LocalStack's Scheduler documentation currently lists schedule execution/target triggering as a limitation.

Therefore:

```text
LocalStack local lab
    └── EventBridge scheduled rules

Real AWS
    └── EventBridge Scheduler
```

For a production AWS implementation, use EventBridge Scheduler for one-time schedules such as "execute this Lambda five minutes from now."

---

# 50. Application-triggered Scheduling

In production, an application can create a schedule:

```text
Spring Boot
    │
    │ CreateSchedule
    ▼
EventBridge Scheduler
    │
    │ wait
    ▼
Lambda
```

For example:

```text
POST /jobs
{
    "executeAfterMinutes": 5
}
```

The application can calculate the target execution time and create a one-time EventBridge Scheduler schedule.

For this local lab, use EventBridge rules for actual schedule execution.

---

# 51. Logging

## Java

Use the Lambda `Context` logger:

```java
context.getLogger().log(
        "Processing transaction"
);
```

Example:

```java
context.getLogger().log(
        "transactionId=" + transactionId
);
```

## Python

Use Python's logging module:

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info(
    "Processing transactionId=%s",
    transaction_id
)
```

---

# 52. View LocalStack Logs

```bash
docker logs lambda-localstack
```

Follow logs:

```bash
docker logs -f lambda-localstack
```

This is useful when debugging:

* Lambda startup
* Lambda invocation
* LocalStack API requests
* EventBridge activity
* Docker-based Lambda execution

---

# 53. Request/Invocation Logs from CLI

AWS CLI can request the Lambda execution log tail for synchronous invocations.

Example:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda invoke \
  --function-name java-hello \
  --log-type Tail \
  --cli-binary-format raw-in-base64-out \
  --payload file://payload.json \
  response.json \
  --query LogResult \
  --output text \
  | base64 --decode
```

---

# 54. Exception Handling

## Java

Example:

```java
try {

    doSomething();

} catch (Exception e) {

    context.getLogger().log(
            "Processing failed: " + e.getMessage()
    );

    throw e;
}
```

The exception should generally be allowed to propagate when the invocation should be considered failed.

---

## Python

```python
try:

    do_something()

except Exception:

    logger.exception(
        "Processing failed"
    )

    raise
```

The important part is:

```python
raise
```

If you catch an exception and return a normal response:

```python
except Exception:
    return {
        "success": False
    }
```

Lambda may consider the invocation successful.

If you re-raise:

```python
except Exception:
    logger.exception("Processing failed")
    raise
```

Lambda knows that the function failed.

---

# 55. Testing an Exception

Modify the Python Lambda temporarily:

```python
def handler(event, context):

    if event.get("fail"):
        raise RuntimeError(
            "Intentional failure"
        )

    return {
        "success": True
    }
```

Invoke:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda invoke \
  --function-name python-hello \
  --invocation-type RequestResponse \
  --cli-binary-format raw-in-base64-out \
  --payload '{"fail":true}' \
  error-response.json
```

Inspect:

```bash
cat error-response.json
```

The invocation response will indicate that the Lambda function failed.

---

# 56. Lambda Invocation vs Function Success

This distinction is important.

There are two different things:

```text
1. Did the Lambda service accept/process the invocation?
2. Did the Lambda handler execute successfully?
```

For example:

```text
Client
  │
  ▼
Lambda service
  │
  ▼
handler()
  │
  X exception
```

The API request itself may have been successfully received while the actual function execution failed.

Always inspect:

* invocation status
* function error
* returned payload
* logs

as appropriate.

---

# 57. Background Task Example

The worker functions intentionally sleep for five seconds:

```python
time.sleep(5)
```

or:

```java
Thread.sleep(5_000);
```

Run:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda invoke \
  --function-name python-worker \
  --invocation-type Event \
  --payload '{"job":"123"}' \
  response.json
```

The CLI gets the acknowledgement immediately:

```json
{
  "StatusCode": 202
}
```

The worker then continues processing.

This demonstrates:

```text
immediate invocation acknowledgement
```

versus:

```text
actual background task completion
```

---

# 58. Getting the Result of a Background Job

Asynchronous Lambda invocation does not give the caller the eventual return value.

For a real application, use a job/status model.

For example:

```text
POST /jobs
```

returns:

```json
{
  "jobId": "job-123",
  "status": "ACCEPTED"
}
```

Worker:

```text
job-123
    │
    ▼
PROCESSING
    │
    ▼
COMPLETED
```

The application can then:

```text
GET /jobs/job-123
```

and receive:

```json
{
  "jobId": "job-123",
  "status": "COMPLETED",
  "result": {
    "processed": 10
  }
}
```

The job state would normally be stored in something such as DynamoDB.

---

# 59. Recommended Production Background Architecture

For production workloads, especially workloads where reliability and retry matter:

```text
                  Client
                    │
                    ▼
              API Gateway
                    │
                    ▼
              Starter Lambda
                    │
                    │ SendMessage
                    ▼
                  SQS
                    │
                    │ event source mapping
                    ▼
              Worker Lambda
                    │
             ┌──────┴──────┐
             ▼             ▼
          DynamoDB        S3
```

If the worker fails:

```text
SQS
 │
 ▼
Worker Lambda
 │
 X failure
 │
 ▼
retry
 │
 X
 │
 ▼
DLQ
```

This is generally more robust than directly invoking another Lambda asynchronously when the workload requires durable queuing.

---

# 60. Lambda Scaling

Lambda is invocation-based rather than a permanently running process.

Conceptually:

```text
1 request

Lambda environment
        │
        ▼
      handler
```

Many concurrent requests:

```text
              ┌── Lambda environment
              ├── Lambda environment
              ├── Lambda environment
              ├── Lambda environment
              └── Lambda environment
```

Lambda can create multiple execution environments.

Therefore downstream services must be capable of handling the resulting concurrency.

Consider:

* reserved concurrency
* provisioned concurrency
* SQS batch size
* maximum concurrency
* database connection limits
* downstream API rate limits

---

# 61. Lambda Execution Environment

A Lambda environment can be reused.

First invocation:

```text
create environment
       │
       ▼
initialize runtime
       │
       ▼
execute handler
```

Later invocation may use the existing environment:

```text
existing environment
       │
       ▼
execute handler
```

But application code must not depend on reuse.

Treat Lambda as stateless.

---

# 62. Temporary Files

Lambda can use its temporary filesystem for temporary processing.

Do not use it as durable application storage.

Use services such as:

```text
S3
DynamoDB
RDS
SQS
```

for persistent state.

---

# 63. Lambda Configuration

In AWS, Lambda can be configured with:

* memory
* timeout
* environment variables
* IAM execution role
* concurrency
* VPC configuration
* layers
* tracing
* dead-letter destinations
* event source mappings

The local lab intentionally keeps these settings minimal.

---

# 64. Useful Makefile

A convenient `Makefile`:

```makefile
AWS = aws --endpoint-url=http://localhost:4566

.PHONY: up down build deploy invoke-java invoke-python logs

up:
	docker compose up -d

down:
	docker compose down

build:
	cd lambdas/java && gradle build
	cp lambdas/java/build/distributions/lambda-java.zip .
	cd lambdas/python && zip -j ../../lambda-python-hello.zip hello_handler.py
	cd lambdas/python && zip -j ../../lambda-python-worker.zip worker_handler.py

deploy:
	./scripts/deploy.sh

schedule:
	./scripts/schedule.sh

invoke-java:
	$(AWS) lambda invoke \
		--function-name java-hello \
		--invocation-type RequestResponse \
		--cli-binary-format raw-in-base64-out \
		--payload file://payload.json \
		response.json
	cat response.json

invoke-python:
	$(AWS) lambda invoke \
		--function-name python-hello \
		--invocation-type RequestResponse \
		--cli-binary-format raw-in-base64-out \
		--payload file://payload.json \
		response.json
	cat response.json

invoke-java-async:
	$(AWS) lambda invoke \
		--function-name java-worker \
		--invocation-type Event \
		--cli-binary-format raw-in-base64-out \
		--payload file://payload.json \
		response.json
	cat response.json

invoke-python-async:
	$(AWS) lambda invoke \
		--function-name python-worker \
		--invocation-type Event \
		--cli-binary-format raw-in-base64-out \
		--payload file://payload.json \
		response.json
	cat response.json

list:
	$(AWS) lambda list-functions \
		--query 'Functions[].FunctionName'

rules:
	$(AWS) events list-rules

logs:
	docker logs -f lambda-localstack
```

---

# 65. Deployment Script

`scripts/deploy.sh`:

```bash
#!/usr/bin/env bash

set -euo pipefail

source "$(dirname "$0")/common.sh"

echo "Creating IAM role..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    iam create-role \
    --role-name lambda-lab-role \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }]
    }' \
    >/dev/null 2>&1 || true


echo "Creating Java Lambda..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda create-function \
    --function-name java-hello \
    --runtime java21 \
    --handler example.HelloHandler \
    --role "$ROLE_ARN" \
    --zip-file fileb://lambda-java.zip \
    >/dev/null 2>&1 || true


echo "Creating Java worker..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda create-function \
    --function-name java-worker \
    --runtime java21 \
    --handler example.WorkerHandler \
    --role "$ROLE_ARN" \
    --zip-file fileb://lambda-java.zip \
    >/dev/null 2>&1 || true


echo "Creating Python Lambda..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda create-function \
    --function-name python-hello \
    --runtime python3.12 \
    --handler hello_handler.handler \
    --role "$ROLE_ARN" \
    --zip-file fileb://lambda-python-hello.zip \
    >/dev/null 2>&1 || true


echo "Creating Python worker..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda create-function \
    --function-name python-worker \
    --runtime python3.12 \
    --handler worker_handler.handler \
    --role "$ROLE_ARN" \
    --zip-file fileb://lambda-python-worker.zip \
    >/dev/null 2>&1 || true


echo
echo "Lambda functions:"

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda list-functions \
    --query 'Functions[].FunctionName'
```

---

# 66. Schedule Script

`scripts/schedule.sh`:

```bash
#!/usr/bin/env bash

set -euo pipefail

source "$(dirname "$0")/common.sh"

echo "Creating Java rate rule..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    events put-rule \
    --name java-lambda-rate \
    --schedule-expression "rate(1 minute)" \
    --state ENABLED


echo "Creating Python rate rule..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    events put-rule \
    --name python-lambda-rate \
    --schedule-expression "rate(1 minute)" \
    --state ENABLED


echo "Creating Java cron rule..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    events put-rule \
    --name java-lambda-cron \
    --schedule-expression "cron(0 * * * ? *)" \
    --state ENABLED


echo "Granting Java rate permission..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda add-permission \
    --function-name java-hello \
    --statement-id java-rate-eventbridge \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn \
    "arn:aws:events:${REGION}:${ACCOUNT_ID}:rule/java-lambda-rate" \
    >/dev/null 2>&1 || true


echo "Granting Python rate permission..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    lambda add-permission \
    --function-name python-hello \
    --statement-id python-rate-eventbridge \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn \
    "arn:aws:events:${REGION}:${ACCOUNT_ID}:rule/python-lambda-rate" \
    >/dev/null 2>&1 || true


echo "Adding Java rate target..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    events put-targets \
    --rule java-lambda-rate \
    --targets "Id=java-lambda,Arn=$JAVA_LAMBDA_ARN"


echo "Adding Python rate target..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    events put-targets \
    --rule python-lambda-rate \
    --targets "Id=python-lambda,Arn=$PYTHON_LAMBDA_ARN"


echo "Adding Java cron target..."

aws \
    --endpoint-url="$LOCALSTACK_URL" \
    events put-targets \
    --rule java-lambda-cron \
    --targets "Id=java-lambda-cron,Arn=$JAVA_LAMBDA_ARN"


echo
echo "Schedules configured."
```

---

# 67. Complete Quick Start

Once all files are in place:

```bash
make up
```

Build:

```bash
make build
```

Deploy:

```bash
make deploy
```

Check functions:

```bash
make list
```

Invoke Java:

```bash
make invoke-java
```

Invoke Python:

```bash
make invoke-python
```

Invoke Java asynchronously:

```bash
make invoke-java-async
```

Invoke Python asynchronously:

```bash
make invoke-python-async
```

Create schedules:

```bash
make schedule
```

View schedules:

```bash
make rules
```

View LocalStack logs:

```bash
make logs
```

Stop LocalStack:

```bash
make down
```

---

# 68. Useful Manual Commands

List Lambda functions:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda list-functions
```

Get a Lambda:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda get-function \
  --function-name java-hello
```

List EventBridge rules:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events list-rules
```

List EventBridge targets:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events list-targets-by-rule \
  --rule java-lambda-rate
```

Delete a rule:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  events delete-rule \
  --name java-lambda-rate
```

Delete a Lambda:

```bash
aws \
  --endpoint-url=http://localhost:4566 \
  lambda delete-function \
  --function-name java-hello
```

---

# 69. LocalStack Reset

To completely remove LocalStack state:

```bash
docker compose down
```

Then remove the local data:

```bash
rm -rf localstack-data
```

Start again:

```bash
docker compose up -d
```

This gives you a clean environment.

---

# 70. Important Difference: LocalStack vs AWS

LocalStack is excellent for:

* local development
* learning AWS APIs
* integration tests
* CI testing
* avoiding AWS costs during development

But:

```text
LocalStack != AWS
```

Always validate production behavior in AWS.

Differences can exist around:

* IAM
* networking
* service integrations
* permissions
* event delivery
* timing
* service-specific features
* Lambda execution
* EventBridge Scheduler

---

# 71. Recommended Production Architecture

For simple scheduled jobs:

```text
EventBridge Scheduler
        │
        ▼
      Lambda
```

For HTTP APIs:

```text
API Gateway
     │
     ▼
  Lambda
     │
     ▼
 DynamoDB
```

For background jobs:

```text
API Gateway
     │
     ▼
Starter Lambda
     │
     ▼
    SQS
     │
     ▼
Worker Lambda
     │
     ├── DynamoDB
     └── S3
```

For file processing:

```text
Client
  │
  ▼
S3
  │
  ▼
Lambda
  │
  ▼
SQS
  │
  ▼
Worker Lambda
```

For periodic processing:

```text
EventBridge Scheduler
        │
        ▼
     Lambda
        │
        ▼
 DynamoDB / S3 / SQS
```

---

# 72. Key Takeaways

## Lambda is invocation based

It is not normally a continuously running application.

```text
event
  ↓
Lambda
  ↓
handler
  ↓
result
```

---

## Synchronous invocation returns the result

```text
RequestResponse
```

```text
Client → Lambda → Result
```

---

## Asynchronous invocation returns immediately

```text
Event
```

```text
Client → Lambda → 202
```

The Lambda's eventual result is not returned to the client.

---

## Do not depend on background threads inside Lambda

Instead use:

```text
SQS
Lambda async invocation
EventBridge
Step Functions
```

depending on the workload.

---

## EventBridge can trigger Lambda

For recurring schedules:

```text
rate(...)
cron(...)
```

For one-time AWS schedules:

```text
at(...)
```

The latter is normally handled through EventBridge Scheduler.

---

## Exceptions matter

If processing fails:

```text
log
+
propagate exception
```

rather than silently returning success.

---

## Logging matters

Use:

```text
Lambda Context logger
Python logging
```

and correlate logs using identifiers such as:

```text
requestId
transactionId
jobId
eventType
```

---

# 73. Suggested Next Step

The next useful extension to this lab is:

```text
                    ┌──────────────┐
                    │ Spring Boot  │
                    └──────┬───────┘
                           │
                           ▼
                     Starter Lambda
                           │
                           ▼
                          SQS
                           │
                           ▼
                     Worker Lambda
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                DynamoDB         S3
                    │
                    ▼
                Job Status
```

That version can demonstrate the production concepts that become important for real backend systems:

* SQS → Lambda event source mapping
* batch processing
* visibility timeout
* retry
* partial batch failure
* dead-letter queue
* idempotency
* DynamoDB job status
* `PENDING → PROCESSING → COMPLETED/FAILED`
* immediate `202 Accepted`
* polling for completion
* scheduled jobs
* Java and Python workers
* LocalStack integration testing

This is a much closer model to a production event-driven AWS architecture than directly invoking a Lambda from another Lambda.

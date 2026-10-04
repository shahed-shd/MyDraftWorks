
logSection "Checking dependencies"

logInfo "Checking Docker version"
docker --version

logInfo "Checking AWS CLI version"
aws --version

logInfo "Checking Java version"
java -version

logInfo "Checking Python version"
python3 --version

logInfo "Checking Gradle version"
cd lambdas/java || exit;
./gradlew --version
# Or, gradle --version

# To create wrapper `gradlew`, run `gradle wrapper` in the project root directory.
# If you don't have gradle installed, you can use the following command to create the wrapper:
# Take the path of some other project root where `gradlew` exists and then run
# `<path-to-gradlew> wrapper`
# or `<path-to-gradlew> wrapper gradle wrapper --gradle-version <gradle-version>`
cd ../..;

# Verify Docker is running
logInfo "Verifying Docker is running"
docker ps

# Verify LocalStack is running
logInfo "Verifying LocalStack is running by checking the health endpoint"
curl http://localhost:4566/_localstack/health | jq .

# Verify AWS CLI can access the running LocalStack
logInfo "Verifying AWS CLI can access the running LocalStack by checking the caller identity"
awslocal sts get-caller-identity | jq .
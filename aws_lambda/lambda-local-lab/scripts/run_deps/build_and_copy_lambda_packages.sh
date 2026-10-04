
logSection "Building lambda packages"
# Build the Java lambda package using Gradle
logInfo "Building Java lambda package using Gradle"

cd lambdas/java || exit
./gradlew build
cd ../..

# Copy the built lambda package to the project root directory
logInfo "Copying built Java lambda package to project root directory"
cp \
  lambdas/java/build/distributions/lambda-java.zip \
  lambda-java.zip

# Build the Python lambda packages in project root directory
logInfo "Building Python lambda packages in project root directory"

cd lambdas/python || exit

zip ../../lambda-python-hello.zip \
    hello_handler.py

zip ../../lambda-python-worker.zip \
    worker_handler.py

cd ../..

# List the generated lambda packages
logSection "Listing generated lambda packages"
ls -lh *.zip

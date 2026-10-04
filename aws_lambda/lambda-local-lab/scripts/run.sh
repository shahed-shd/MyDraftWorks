# ========== Commons ==========
source run_deps/common_configs.sh
source run_deps/common_functions.sh
# ========== Commons done ==========

# ========== Navigate to root dir ==========
logSection "Navigating to project root directory"
cd ..
logInfo "Current directory: $(pwd)"

RUN_DEPS_DIR_FROM_ROOT="scripts/run_deps"
# ========== Navigate to root dir done ==========

# ========== Checking prerequisites ==========
source ${RUN_DEPS_DIR_FROM_ROOT}/check_prerequisites.sh
# ========== Checking prerequisites done ==========

# ========== Build lambda packages ==========
source ${RUN_DEPS_DIR_FROM_ROOT}/build_and_copy_lambda_packages.sh
# ========== Build lambda packages done ==========

# ========== Create IAM Role ==========
source ${RUN_DEPS_DIR_FROM_ROOT}/create_iam_role.sh
# ========== Create IAM Role done ==========

# ========== Create Lambdas ==========
source ${RUN_DEPS_DIR_FROM_ROOT}/create_lambdas.sh
# ========== Create Lambdas done ==========

# ========== CLI Invocation ==========
source ${RUN_DEPS_DIR_FROM_ROOT}/cli_invocation.sh
# ========== CLI Invocation done ==========

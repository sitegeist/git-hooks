#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUTPUT_DIR="../tests/output"

source $SCRIPT_DIR/../utils/afterEach
source $SCRIPT_DIR/../utils/beforeEach

#
# Tests for a commit message without prefix tags.
#
testOutputForCommitMessageWithoutPrimaryPrefix() {
	beforeEach

	# Install all hooks.
	hook > /dev/null

	# Commit the test file.
	echo "test" > test_file
	git add test_file

	OUTPUT=$(git commit -m "My commit message." 2>&1)
	echo $OUTPUT > "$OUTPUT_DIR/prepare-commit-msg.result.txt"

	diff "$OUTPUT_DIR/prepare-commit-msg.result.txt" "$OUTPUT_DIR/prepare-commit-msg.txt"
	assertEquals "The prepare-commit-msg should output a commit-msg guide if no prefix tags are found within the commit msg." 0 $?

	afterEach
}
testReturnCodeForCommitMessageWithoutPrimaryPrefix() {
	beforeEach

	# Install all hooks.
	hook > /dev/null

	# Commit the test file.
	echo "test" > test_file
	git add test_file
	git commit -m "My commit message." > /dev/null 2>&1
	returnCode=$?
	assertEquals "The prepare-commit-msg hook exit with an error code if no primary or secondary prefix was found." 1 $returnCode

	afterEach
}

#
# Finally, run all tests.
#
. shunit2

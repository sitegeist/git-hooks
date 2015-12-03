#!/usr/bin/env bash

#
# Tests for the pre-commit hook.
#
# Author: Tyll Weiß <weiss@sitegeist.de>
#
HOOK_DIR="$HOME/.sitegeist-hooks"
TEST_WORKING_DIR="$BASE_DIR/test_working_dir"

source $HOOK_DIR/utils/afterEach
source $HOOK_DIR/utils/beforeEach

#
# Sets up the test directory
#
installLinters() {
	echo '{
  "name": "test_working_dir",
  "version": "0.0.1",
  "description": "",
  "author": "",
  "license": "ISC",
  "dependencies": {
    "xo": "*"
  }
}' > package.json
	npm install > /dev/null 2>&1
}

#
# Test if we can commit without changes to .js files.
#
testCommitWithoutJavaScriptChanges() {
	beforeEach

	hook install > /dev/null

	# Install the linters.
	installLinters

	echo "test" > "test.txt"
	git add test.txt
	git commit -m "[TASK] Add a test file." > /dev/null 2>&1
	assertEquals "The pre-commit hook should exit with an success code if no .js files are within the changed files." 0 $?

	afterEach
}

#
# Test if the hooks aborts if we commit js changes with errors.
#
testCommitWithInvalidJavaScriptChanges() {
	beforeEach

	hook install > /dev/null

	# Install the linters.
	installLinters

	echo "test" > "test.js"
	git add test.js
	git commit -m "[TASK] Add a test js file." > /dev/null 2>&1
	assertEquals "The pre-commit hook should exit with an error code if errors are found within the changed .js files." 1 $?

	afterEach
}

#
# Test if the hooks aborts if we commit js changes with errors.
#
testCommitWithValidJavaScriptChanges() {
	beforeEach

	hook install > /dev/null

	# Install the linters.
	installLinters

	echo "console.log('test');" > "test.js"
	git add test.js
	git commit -m "[TASK] Add a test js file." > /dev/null 2>&1
	assertEquals "The pre-commit hook should exit with an success code if no errors are found within the changed .js files." 0 $?

	afterEach
}

#
# Finally, run all tests.
#
. shunit2

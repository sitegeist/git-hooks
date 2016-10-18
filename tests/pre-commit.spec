#!/usr/bin/env bash

#
# Tests for the pre-commit hook.
#
# Author: Tyll Weiß <weiss@sitegeist.de>, Max Strübing <struebing@sitegeist.de>
#
HOOK_DIR="$HOME/.sitegeist-hooks"
TEST_WORKING_DIR="$BASE_DIR/test_working_dir"

source $HOOK_DIR/utils/afterEach
source $HOOK_DIR/utils/beforeEach
source $HOOK_DIR/utils/fileExists

#
# Sets up the test directory
#
function installLinters() {
	echo '{
  "name": "test_working_dir",
  "version": "0.0.1",
  "description": "",
  "author": "",
  "license": "ISC",
  "dependencies": {
    "xo": "0.16.0"
  }
}' > package.json
	npm install > /dev/null 2>&1
}

#
# Sets up the extended hook.
#
function setupHookExtension() {
	echo 'extend:' >> .hook.yml
	echo '  pre_commit: hookExtensions/pre-commit' >> .hook.yml

	mkdir hookExtensions
	touch hookExtensions/pre-commit
	chmod +x hookExtensions/pre-commit
}

#
# Test if we can commit without changes to .js files.
#
function testCommitWithoutJavaScriptChanges() {
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
function testCommitWithInvalidJavaScriptChanges() {
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
# Test if the hook successfully aborts if we commit js changes without errors.
#
function testCommitWithValidJavaScriptChanges() {
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
# Test the creation of the npm shrinkwrap file if the package.json has changed.
#
function testCreationOfNpmShrinkwrapFile() {
	beforeEach

	hook install > /dev/null

	echo '{
	"name": "test_working_dir",
	"version": "0.0.1",
	"description": "",
	"author": "",
	"license": "ISC",
	"dependencies": {
		"page": "*"
	}
}' > package.json
	git add package.json
	git commit -m "[TASK] Add a npm dependency." > /dev/null 2>&1

	fileExists "$TEST_WORKING_DIR/npm-shrinkwrap.json"
	returnCode=$?
	assertEquals "The npm-shrinkwrap file should be created." 1 $returnCode

	afterEach
}

#
# Test the return code bubble for extended hooks.
#
function testReturnCodeForFailingHookExtension() {
	beforeEach

	hook install > /dev/null

	setupHookExtension

	echo 'exit 1' > hookExtensions/pre-commit
	git add hookExtensions/pre-commit .hook.yml
	git commit -m "[TASK] Commit hook extensions." > /dev/null 2>&1
	returnCode=$?
	assertEquals "The pre-commit hook should exit with code 1 if the extension exits with code 1." 1 $returnCode

	echo 'exit 0' > hookExtensions/pre-commit
	git commit -m "[TASK] Commit hook extensions." > /dev/null 2>&1
	returnCode=$?
	assertEquals "The pre-commit hook should exit with code 0 if the extension exits with code 0." 0 $returnCode

	afterEach
}

#
# Finally, run all tests.
#
. shunit2

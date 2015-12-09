#!/usr/bin/env bash

#
# Tests for the prepare-commit-msg hook.
#
# Author: Tyll Weiß <weiss@sitegeist.de>
#
HOOK_DIR="$HOME/.sitegeist-hooks"
OUTPUT_DIR="$HOOK_DIR/tests/output"

source $HOOK_DIR/utils/afterEach
source $HOOK_DIR/utils/beforeEach

#
# Helper function to leanen the tests.
#
function modifyTestFile() {
	echo "test" >> test_file
	git add test_file
}

#
# Tests for a commit message without prefix tags.
#
function testOutputForCommitMessageWithoutPrimaryPrefix() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# Commit the test file.
	modifyTestFile

	OUTPUT=$(git commit -m "My commit message." 2>&1)
	echo $OUTPUT > "$OUTPUT_DIR/prepare-commit-msg.result.txt"

	diff "$OUTPUT_DIR/prepare-commit-msg.result.txt" "$OUTPUT_DIR/prepare-commit-msg.txt"
	assertEquals "The prepare-commit-msg should output a commit-msg guide if no prefix tags are found within the commit msg." 0 $?

	afterEach
}
function testReturnCodeForCommitMessageWithoutPrimaryPrefix() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# Commit the test file.
	modifyTestFile
	git commit -m "My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if no primary or secondary prefix was found." 1 $?

	afterEach
}
function testReturnCodeForCommitMessageWithInvalidPrefix() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# Invalid/Custom prefix, which is not covered by the TYPO3 commit guidelines.
	modifyTestFile
	git commit -m "[MyPrefix] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if an invalid prefix was found." 1 $?

	# Invalid [TASK] prefix.
	modifyTestFile
	git commit -m "[TASK My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if an incomplete prefix was found." 1 $?

	# Missing space between the prefix and the message.
	modifyTestFile
	git commit -m "[TASK]My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if no space was found between the prefix and the message." 1 $?

	afterEach
}
function testReturnCodeForCommitMessageWithPrimaryPrefixes() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# Test the [FEATURE] prefix.
	modifyTestFile
	git commit -m "[FEATURE] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [FEATURE] prefix was found." 0 $?

	# Test the [TASK] prefix.
	modifyTestFile
	git commit -m "[TASK] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [TASK] prefix was found." 0 $?

	# Test the [BUGFIX] prefix.
	modifyTestFile
	git commit -m "[BUGFIX] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [BUGFIX] prefix was found." 0 $?

	# Test the [DOCS] prefix.
	modifyTestFile
	git commit -m "[DOCS] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [DOCS] prefix was found." 0 $?

	# Test the [CLEANUP] prefix.
	modifyTestFile
	git commit -m "[CLEANUP] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [CLEANUP] prefix was found." 0 $?

	afterEach
}
function testReturnCodeForCommitMessageWithInvalidSecondaryPrefixes() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# Test the [!!!] prefix.
	modifyTestFile
	git commit -m "[!!!] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if the [!!!] prefix was found but no primary is followed directly after." 1 $?

	# Test the [WIP] prefix.
	modifyTestFile
	git commit -m "[WIP] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if the [WIP] prefix was found but no primary is followed directly after." 1 $?

	# Test the an invalid secondary prefix with an valid primary one.
	modifyTestFile
	git commit -m "[FAQ][TASK] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an error code if an invalid secondary prefix and a valid primary is followed directly after." 1 $?

	afterEach
}
function testReturnCodeForCommitMessageWithSecondaryPrefixes() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# Test the [!!!][FEATURE] prefix.
	modifyTestFile
	git commit -m "[!!!][FEATURE] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [!!!][FEATURE] prefixes where found." 0 $?

	# Test the [!!!][TASK] prefix.
	modifyTestFile
	git commit -m "[!!!][TASK] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [!!!][TASK] prefixes where found." 0 $?

	# Test the [!!!][BUGFIX] prefix.
	modifyTestFile
	git commit -m "[!!!][BUGFIX] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [!!!][BUGFIX] prefix was found." 0 $?

	# Test the [!!!][DOCS] prefix.
	modifyTestFile
	git commit -m "[!!!][DOCS] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [!!!][DOCS] prefix was found." 0 $?

	# Test the [!!!][CLEANUP] prefix.
	modifyTestFile
	git commit -m "[!!!][CLEANUP] My commit message." > /dev/null 2>&1
	assertEquals "The prepare-commit-msg hook should exit with an success code if the [!!!][CLEANUP] prefix was found." 0 $?

	afterEach
}
function testAppendedIssueNumberFromBranchName() {
	beforeEach

	# Install all hooks.
	hook install > /dev/null

	# First, check if the issue number will be appended while commiting in a feature branch.
	git checkout --quiet -b task/21993/myFeature
	modifyTestFile
	git commit -m "[TASK] My commit message." > /dev/null 2>&1

	COMMIT_WITH_APPENDED_ISSUE_NUMBER=$(git log --grep="refs #21993")
	assertNotNull "$COMMIT_WITH_APPENDED_ISSUE_NUMBER"

	# Afterwards, we should test the opposite case. The hook should not append the issue number if not in a feature branch.
	git checkout master --quiet
	git checkout --quiet -b task/myFeature
	modifyTestFile
	git commit -m "[TASK] My commit message." > /dev/null 2>&1

	COMMIT_WITH_APPENDED_ISSUE_NUMBER=$(git log --grep="refs #21993")
	assertNull "$COMMIT_WITH_APPENDED_ISSUE_NUMBER"

	afterEach
}

#
# Finally, run all tests.
#
. shunit2

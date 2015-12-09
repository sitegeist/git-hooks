#!/usr/bin/env bash

#
# Tests for the hook CLI.
#
# Author: Tyll Weiß <weiss@sitegeist.de>
#
HOOK_DIR="$HOME/.sitegeist-hooks"
OUTPUT_DIR="$HOOK_DIR/tests/output"

source $HOOK_DIR/utils/afterEach
source $HOOK_DIR/utils/beforeEach
source $HOOK_DIR/utils/fileExists
source $HOOK_DIR/utils/isFileSymlink

#
# Tests for an invalid argument
#
function testReturnCodeForInvalidCommand() {
	beforeEach

	hook invalid_argument > /dev/null
	assertEquals "The Hook CLI should return a failure code if ran with an invalid argument." 1 $?

	afterEach
}

#
# Tests for the installation of hooks.
#
function testPresenceOfHooks() {
	beforeEach

	hook install > /dev/null

	#
	# post-merge
	#
	fileExists ".git/hooks/post-merge"
	returnCode=$?
	assertEquals "The post-merge hook should be in place." 0 $returnCode

	isFileSymlink ".git/hooks/post-merge"
	returnCode=$?
	assertEquals "The post-merge hook should be a symbolic link." 0 $returnCode

	#
	# pre-commit
	#
	fileExists ".git/hooks/pre-commit"
	returnCode=$?
	assertEquals "The pre-commit hook should be in place." 0 $returnCode

	isFileSymlink ".git/hooks/pre-commit"
	returnCode=$?
	assertEquals "The pre-commit hook should be a symbolic link." 0 $returnCode

	#
	# pre-commit
	#
	fileExists ".git/hooks/prepare-commit-msg"
	returnCode=$?
	assertEquals "The prepare-commit-msg hook should be in place." 0 $returnCode

	isFileSymlink ".git/hooks/prepare-commit-msg"
	returnCode=$?
	assertEquals "The prepare-commit-msg hook should be a symbolic link." 0 $returnCode

	afterEach
}

function testReturnCodeWithoutArguments() {
	beforeEach

	hook install > /dev/null
	returnCode=$?
	assertEquals "The Hook CLI should return a success code if ran without arguments." 0 $returnCode

	afterEach
}

#
# Tests for the 'help' command.
#
function testOutputForHelpCommand() {
	beforeEach

	hook help > "$OUTPUT_DIR/help.result.txt"

	diff "$OUTPUT_DIR/help.result.txt" "$OUTPUT_DIR/help.txt"
	assertEquals "The Hook CLI should output a instructional guide if ran with the 'help' argument." 0 $?

	afterEach
}

function testReturnCodeForHelpCommand() {
	beforeEach

	hook help > /dev/null
	returnCode=$?
	assertEquals "The Hook CLI should return a success code if ran with the 'help' argument." 0 $returnCode

	afterEach
}

#
# Tests for the 'help:hooks' command.
#
function testOutputForHelpHooksCommand() {
	beforeEach

	hook help:hooks > "$OUTPUT_DIR/help_hooks.result.txt"

	diff "$OUTPUT_DIR/help_hooks.result.txt" "$OUTPUT_DIR/help_hooks.txt"
	assertEquals "The Hook CLI should output a instructional guide if ran with the 'help:hooks' argument." 0 $?

	afterEach
}

function testReturnCodeForHelpHooksCommand() {
	beforeEach

	hook help:hooks > /dev/null
	returnCode=$?
	assertEquals "The Hook CLI should return a success code if ran with the 'help:hooks' argument." 0 $returnCode

	afterEach
}

#
# Tests for the self-update command.
#
function testReturnCodeForSelfUpdateCommand() {
	beforeEach

	hook help self-update > /dev/null
	returnCode=$?
	assertEquals "The Hook CLI should return a success code if ran with the 'self-update' argument." 0 $returnCode

	afterEach
}

#
# Finally, run all tests.
#
. shunit2

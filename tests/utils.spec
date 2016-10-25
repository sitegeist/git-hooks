#!/usr/bin/env bash

#
# Tests for the util functions.
#
# Author: Max Strübing <struebing@sitegeist.de>
#
HOOK_DIR="$HOME/.sitegeist-hooks"
OUTPUT_DIR="$HOOK_DIR/tests/output"

source $HOOK_DIR/utils/afterEach
source $HOOK_DIR/utils/beforeEach
source $HOOK_DIR/utils/fileExists
source $HOOK_DIR/utils/isFileExecutable
source $HOOK_DIR/utils/isFileSymlink

#
# Tests fileExists
#
function testFileExists() {
    beforeEach

    FILENAME=$(date +%s)
    touch $FILENAME
    fileExists $FILENAME
    assertEquals "fileExists should return a success value if a file exists" 0 $?
    rm $FILENAME

    FILENAME=$(date +%s)
    fileExists $FILENAME
    assertEquals "fileExists should return an error code if a file not exists" 1 $?
    
    afterEach
}

#
# Tests isFileExecutable
#
function testIsFileExecutable() {
    beforeEach

    FILENAME=$(date +%s)
    touch $FILENAME
    chmod +x $FILENAME
    isFileExecutable $FILENAME
    assertEquals "isFileExecutable should return a success value if a file is executable" 0 $?
    rm $FILENAME

    FILENAME=$(date +%s)
    touch $FILENAME
    isFileExecutable $FILENAME
    assertEquals "isFileExecutable should return an error value if a file is not executable" 1 $?
    rm $FILENAME

    afterEach
}

#
# Tests isFileSymlink
#
function testIsFileSymlink() {
    beforeEach

    FILENAME=$(date +%s)
    SYMLINK="symlink-$FILENAME"
    touch $FILENAME
    ln -s $FILENAME $SYMLINK
    isFileSymlink $SYMLINK
    assertEquals "isFileSymlink should return a success value if a file is a symlink" 0 $?
    rm $FILENAME
    rm $SYMLINK

    FILENAME=$(date +%s)
    touch $FILENAME
    isFileSymlink $FILENAME
    assertEquals "isFileSymlink should return an error value if a file is not a symlink" 1 $?
    rm $FILENAME

    afterEach
}

#
# Finally, run all tests.
#
. shunit2

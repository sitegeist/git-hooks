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

#
# Tests fileExists
#
function testFileExists() {
    beforeEach

    FILENAME=$(date +%s )
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
# Finally, run all tests.
#
. shunit2

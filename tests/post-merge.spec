#!/usr/bin/env bash

#
# Tests for the post-merge hook.
#
# Author: Tyll Weiß <weiss@sitegeist.de>
#
HOOK_DIR="$HOME/.sitegeist-hooks"
TEST_WORKING_DIR="$BASE_DIR/test_working_dir"

source $HOOK_DIR/utils/afterEach
source $HOOK_DIR/utils/beforeEach

#
# Tests for the automatic update mechanism of node dependencies.
#
testAutomaticUpdateOfNodeDependenciesWithChanges() {
	beforeEach

	hook install > /dev/null

	# Commit a package.json update on another branch.
	git checkout --quiet -b updateNodeDependencies
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

	# We need to install the deps before commiting, since the npm-shrinkwrap command would throw an error otherwise.
	npm install > /dev/null 2>&1

	# Commit the changes.
	git add package.json > /dev/null 2>&1
	git commit -m "[TASK] Add a package.json" > /dev/null 2>&1

	# Remove the previous installed deps, to test if the post-merge hooks actually works.
	rm -rf node_modules > /dev/null 2>&1

	# Merge the update branch, after merging, the node_modules folder should include the dependencies.
	git checkout master --quiet > /dev/null 2>&1
	git merge updateNodeDependencies > /dev/null 2>&1

	DEPENDENCIES=$(ls $TEST_WORKING_DIR/node_modules)
	assertNotNull "$DEPENDENCIES"

	afterEach
}

testAutomaticUpdateOfNodeDependenciesWithoutChanges() {
	beforeEach

	hook install > /dev/null

	# Commit unrelevant changes.
	git checkout --quiet -b anotherBranch
	echo "test" >> test_file
	git add test_file
	git commit -m "[TASK] Commit some files" > /dev/null 2>&1

	# Merge the update branch, after merging, the node_modules folder should include the dependencies.
	git checkout master --quiet
	git merge anotherBranch > /dev/null 2>&1

	DEPENDENCIES=$(ls $TEST_WORKING_DIR/node_modules)
	assertNull "$DEPENDENCIES"

	afterEach
}

#
# Finally, run all tests.
#
. shunit2

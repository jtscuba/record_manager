#!/usr/bin/env bash

set -o pipefail
set -e

if [[ -z "$PROJECT_ROOT" ]]; then
    echo "the PROJECT_ROOT variable is unset" && exit 1
fi

CLI_COMMAND="python ${PROJECT_ROOT}/record_cli.py"

for test_directory in test_cases/*/; do
    echo "----$test_directory----"

    $CLI_COMMAND "$test_directory/comma_separated.txt" \
    "$test_directory/pipe_separated.txt" \
    "$test_directory/space_separated.txt" \
    $(cat $test_directory/order.txt) | \
    diff "$test_directory/expected_output.txt" -

done

echo "all tests passed!"
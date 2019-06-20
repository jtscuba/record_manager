#!/usr/bin/env bash

set -o pipefail
set -e

PROJECT_ROOT="/Users/josh/PycharmProjects/record_manager/"
CLI_COMMAND="python ${PROJECT_ROOT}/record_cli.py"

for test_directory in test_cases/*/; do
    $CLI_COMMAND "$test_directory/comma_separated.txt" \
    "$test_directory/pipe_separated.txt" \
    "$test_directory/space_separated.txt" \
     "last_name_descending" | \
     diff "$test_directory/expected_output.txt" -

done
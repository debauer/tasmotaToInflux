#!/bin/bash

if [[ $1 == "--check" ]]; then
    isort_options="--check-only"
    black_options="--check --diff"
fi

EXIT_CODE=0

isort --quiet ${isort_options:-} ./ || EXIT_CODE=1
black ${black_options:-} */ || EXIT_CODE=1

exit $EXIT_CODE

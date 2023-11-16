#!/bin/bash

if [[ $1 == "--coverage" ]]; then
    coverage_options="--cov-branch --cov-report=term --cov-report=html --cov-report=xml --cov=src"
    shift
fi

if [[ $1 == "--junit" ]]; then
    junit_option="--junitxml xunit-reports/xunit-result-pytest.xml"
    shift
fi

pytest \
    -v \
    ${coverage_options:-} \
    ${junit_option:-} \
    tests/unit "$@"

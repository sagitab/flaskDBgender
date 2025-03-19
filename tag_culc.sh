#!/bin/bash

run_number="$1"

# Ensure run_number is a valid integer and within range
if (( run_number >= 1000 )); then
    exit 1
fi

# Extract digits
units=$(( run_number % 10 ))
run_number=$(( run_number / 10 ))
tens=$(( run_number % 10 ))
run_number=$(( run_number / 10 ))
hundreds=$(( run_number % 10 ))

# Construct and return the formatted string
echo "$hundreds.$tens.$units"

#!/usr/bin/env bash
set -euo pipefail

output=$(./build/autofactory || test $? -eq 1)

grep -q "Machine 7: ALARM" <<< "$output"
grep -q "temperature limit exceeded" <<< "$output"

echo "PASS: thermal interlock"
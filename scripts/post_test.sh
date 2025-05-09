#!/bin/bash
TOOL=$1
if [ -z "$TOOL" ]; then
  echo "Usage: ./post_test.sh selenium|playwright"
  exit 1
fi
python scripts/move_test_report.py $TOOL


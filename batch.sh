#!/bin/sh

set -xe

for file in $(ls output); do
  echo ""
  content=$(cat output/${file}/story.txt)
  python3 run.py output/${file} "$content"
done

echo "Batch complete"
exit 0

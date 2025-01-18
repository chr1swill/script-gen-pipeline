#!/bin/sh

set -xe

for dir in $(ls output); do
  echo "[ ] $dir" >> schedule.txt
  echo "Added $dir to schedule.txt"
done

echo "Added all post to to schedule.txt"
exit 0

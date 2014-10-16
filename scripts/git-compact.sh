#!/bin/bash

BEFORE="$(du -chs .git | grep git)"

rm -rf .git/refs/original/
git reflog expire --expire=now --all
git fsck --full --unreachable
git repack -A -d
git gc --aggressive --prune=now

AFTER="$(du -chs .git | grep git)"

echo ">>> before: ${BEFORE}"
echo ">>> after : ${AFTER}"

#!/bin/sh
# Builds expected.out from real Lua 5.4: runs each script the way
# mini_lua.kara does, in the same order, from this directory, so the
# chunk names in error messages ("scripts/errors.lua:4:") agree.
set -e
cd "$(dirname "$0")"
for s in basics closures tables oop strings errors logs; do
  echo "== scripts/$s.lua"
  lua5.4 "scripts/$s.lua"
done
rm -f report.txt

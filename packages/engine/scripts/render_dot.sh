#!/bin/bash
set -euo pipefail

dot="$1"
stem="$(dirname "$1")/$(basename "$1" .dot)"

dot < "$dot"|
  gvcolor |
  tee >(neato -n -Tsvg -o "$stem.svg") |
  neato -n -Tpng -o "$stem.png"

open "$stem.svg"

echo "Generated: $stem.svg, $stem.png"

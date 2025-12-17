#!/bin/bash
set -euo pipefail

dot="$1"
stem="$(dirname "$1")/$(basename "$1" .dot)"

fdp < "$dot"|
  gvcolor |
  tee >(fdp -Tsvg -o "$stem.svg") |
  fdp -Tpng -o "$stem.png"

open "$stem.svg"

echo "Generated: $stem.svg, $stem.png"

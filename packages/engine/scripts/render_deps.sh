#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."
dot="./tmp/dep_clusters.dot"

mkdir -p tmp
./scripts/dep_clusters.py > "$dot"
./scripts/render_dot.sh "$dot"

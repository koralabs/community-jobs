#!/usr/bin/env bash
# Local test run recorded by adahandle-deployments/common/test-evidence.sh (replaces the old Actions tests).
set -euo pipefail
( set -e; ! git grep -nE '^(<<<<<<<|>>>>>>>) ' -- . ':!*.md' )
( set -e; git ls-files '*.json' | xargs -r -n1 python3 -m json.tool > /dev/null )

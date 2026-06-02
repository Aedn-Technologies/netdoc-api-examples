#!/usr/bin/env bash
# List all devices known to NetDoc Pro.
# Requires curl and jq. Works on WSL; Linux/macOS require a tunnel to the Windows host.

set -euo pipefail

HOST="${NETDOC_HOST:-http://localhost:9742}"
TOKEN="${NETDOC_TOKEN:-your-token-here}"

curl -sS -H "Authorization: Bearer $TOKEN" "$HOST/api/v1/devices" \
  | jq -r '.[] | [.label, .ip, .type, .model] | @tsv' \
  | column -t -s $'\t'

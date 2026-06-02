#!/usr/bin/env bash
# Search NetDoc Pro devices by label, IP, model, type, VLAN, or status.
# Filtering is done client-side against the full device list.
# Requires curl and jq. Works on WSL; Linux/macOS require a tunnel to the Windows host.
#
# Usage: ./search_devices.sh <query>
#   ./search_devices.sh cisco
#   ./search_devices.sh 10.0.99

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <query>" >&2
    exit 1
fi

QUERY="$1"
HOST="${NETDOC_HOST:-http://localhost:9742}"
TOKEN="${NETDOC_TOKEN:-your-token-here}"

curl -sS -H "Authorization: Bearer $TOKEN" "$HOST/api/v1/devices" \
  | jq -r --arg q "$QUERY" '
      [ .[] | select(
          (.label    // "" | test($q; "i")) or
          (.ip       // "" | test($q; "i")) or
          (.model    // "" | test($q; "i")) or
          (.type     // "" | test($q; "i")) or
          (.vlan     // "" | test($q; "i")) or
          (.status   // "" | test($q; "i")) or
          (.diagName // "" | test($q; "i"))
      )] |
      if length == 0 then "No matching devices." | halt_error(0)
      else
        (["Label","IP","Type","Model"] | @tsv),
        (.[] | [.label, .ip, .type, .model] | @tsv)
      end
    ' \
  | column -t -s $'\t'

#!/usr/bin/env python3
"""List all devices known to NetDoc Pro."""

import os
import json
import urllib.request

NETDOC_HOST = os.environ.get("NETDOC_HOST", "http://localhost:9742")
TOKEN = os.environ.get("NETDOC_TOKEN", "your-token-here")


def fetch(path):
    req = urllib.request.Request(
        f"{NETDOC_HOST}{path}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def main():
    devices = fetch("/api/v1/devices")
    print(f"{'Label':<25} {'IP':<16} {'Type':<12} {'Model'}")
    print("-" * 70)
    for d in devices:
        print(f"{d.get('label', ''):<25} {d.get('ip', ''):<16} {d.get('type', ''):<12} {d.get('model', '')}")


if __name__ == "__main__":
    main()

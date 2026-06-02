#!/usr/bin/env python3
"""Export the full device inventory to CSV."""

import os
import csv
import sys
import json
import urllib.request

NETDOC_HOST = os.environ.get("NETDOC_HOST", "http://localhost:9742")
TOKEN = os.environ.get("NETDOC_TOKEN", "your-token-here")


def fetch_devices():
    req = urllib.request.Request(
        f"{NETDOC_HOST}/api/v1/devices",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def main():
    devices = fetch_devices()
    if not devices:
        print("No devices in inventory.")
        sys.exit(0)

    fieldnames = ["label", "ip", "type", "model", "vlan", "status", "diagName"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for device in devices:
        writer.writerow(device)


if __name__ == "__main__":
    main()

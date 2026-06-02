#!/usr/bin/env python3
"""Ansible dynamic inventory script for NetDoc Pro.

Outputs devices from the NetDoc Pro REST API in Ansible inventory format,
grouped by device type AND by VLAN. The VLAN grouping is done client-side
because the server's /api/v1/inventory endpoint groups by type only.

Set NETDOC_HOST and NETDOC_TOKEN environment variables before use.
"""

import os
import sys
import json
import urllib.request

NETDOC_HOST = os.environ.get("NETDOC_HOST", "http://localhost:9742")
TOKEN = os.environ.get("NETDOC_TOKEN", "")


def fetch_devices():
    if not TOKEN:
        print("Error: NETDOC_TOKEN environment variable is required.", file=sys.stderr)
        sys.exit(1)

    req = urllib.request.Request(
        f"{NETDOC_HOST}/api/v1/devices",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read())
    except Exception as exc:
        print(f"Error: Failed to fetch devices from NetDoc Pro: {exc}", file=sys.stderr)
        sys.exit(1)


def build_inventory(devices):
    inventory = {"_meta": {"hostvars": {}}, "all": {"children": []}}
    type_groups = {}
    vlan_groups = {}

    for device in devices:
        # Prefer the label as the inventory hostname; fall back to IP.
        host = device.get("label") or device.get("ip")
        if not host:
            continue

        hostvars = {}
        ip = device.get("ip")
        if ip:
            hostvars["ansible_host"] = ip
        if device.get("vlan"):
            hostvars["netdoc_vlan"] = device["vlan"]
        if device.get("model"):
            hostvars["netdoc_model"] = device["model"]
        if device.get("type"):
            hostvars["netdoc_type"] = device["type"]
        if device.get("status"):
            hostvars["netdoc_status"] = device["status"]
        if device.get("diagName"):
            hostvars["netdoc_diagram"] = device["diagName"]

        inventory["_meta"]["hostvars"][host] = hostvars

        dtype = device.get("type", "Unknown")
        type_groups.setdefault(dtype, []).append(host)

        vlan = device.get("vlan")
        if vlan:
            vlan_groups.setdefault(f"vlan_{vlan}", []).append(host)

    for group, hosts in type_groups.items():
        inventory[group] = {"hosts": hosts}
        inventory["all"]["children"].append(group)

    for group, hosts in vlan_groups.items():
        inventory[group] = {"hosts": hosts}
        inventory["all"]["children"].append(group)

    return inventory


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--host":
        # _meta is populated in --list, so --host can return empty.
        print(json.dumps({}))
        return

    devices = fetch_devices()
    inventory = build_inventory(devices)
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
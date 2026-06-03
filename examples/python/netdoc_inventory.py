#!/usr/bin/env python3
"""Ansible dynamic inventory script for NetDoc Pro.

Outputs devices from the NetDoc Pro REST API in Ansible dynamic inventory
format, grouped by device type and VLAN.

Set NETDOC_HOST and NETDOC_TOKEN environment variables before use.

Usage:
    ansible-inventory -i netdoc_inventory.py --list
    ansible-playbook -i netdoc_inventory.py playbook.yml --limit Switch
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
        hostname = device.get("label") or device.get("ip")
        if not hostname:
            continue

        ip = device.get("ip")
        if ip:
            inventory["_meta"]["hostvars"][hostname] = {
                "ansible_host": ip,
                "type":         device.get("type", ""),
                "vlan":         device.get("vlan", ""),
                "model":        device.get("model", ""),
                "status":       device.get("status", ""),
                "diagName":     device.get("diagName", ""),
            }

        dtype = device.get("type", "unknown")
        type_groups.setdefault(dtype, []).append(hostname)

        vlan = device.get("vlan")
        if vlan:
            vlan_groups.setdefault(f"vlan_{vlan}", []).append(hostname)

    for group, hosts in type_groups.items():
        inventory[group] = {"hosts": hosts}
        inventory["all"]["children"].append(group)

    for group, hosts in vlan_groups.items():
        inventory[group] = {"hosts": hosts}
        inventory["all"]["children"].append(group)

    return inventory


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--host":
        print(json.dumps({}))
        return

    devices = fetch_devices()
    inventory = build_inventory(devices)
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()

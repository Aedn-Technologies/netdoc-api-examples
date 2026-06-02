\# Ansible dynamic inventory



`netdoc\_inventory.py` is a drop-in Ansible dynamic inventory script that pulls devices from NetDoc Pro and groups them by device type and VLAN.



\## Two ways to use NetDoc Pro with Ansible



\*\*Option 1 — Server endpoint directly.\*\* NetDoc Pro's `/api/v1/inventory` endpoint produces valid Ansible dynamic inventory. Group by device type only:



```bash

ansible-inventory -i http://localhost:9742/api/v1/inventory --list

```



This is the simplest path. No script required.



\*\*Option 2 — This script, for extra grouping.\*\* `netdoc\_inventory.py` fetches `/api/v1/devices` and builds inventory \*\*grouped by both device type and VLAN\*\*. The VLAN grouping is done client-side because the server endpoint does not provide it.



Use this script if you want to target hosts by VLAN with `--limit vlan\_10` or similar.



\## Setup



1\. Copy `netdoc\_inventory.py` to your Ansible inventory directory.

2\. Make it executable: `chmod +x netdoc\_inventory.py`

3\. Set environment variables: `NETDOC\_HOST` and `NETDOC\_TOKEN`.



\## Usage



```bash

\# List all hosts grouped by device type and VLAN

ansible-inventory -i netdoc\_inventory.py --list



\# Run a playbook against all switches (group name is the device type as

\# stored in NetDoc Pro — title case, e.g. "Switch" not "switch")

ansible-playbook -i netdoc\_inventory.py update\_switches.yml --limit Switch



\# Or target a VLAN

ansible-playbook -i netdoc\_inventory.py audit\_vlan10.yml --limit vlan\_10

```



Each host has its IP set as `ansible\_host` and its NetDoc Pro label as the inventory hostname.



\## Connection from non-Windows control nodes



NetDoc Pro binds to `127.0.0.1:9742`. To use this inventory script from a Linux or macOS Ansible control node, set up an SSH tunnel to the Windows host first:



```bash

ssh -L 9742:localhost:9742 user@windows-host

```



Then set `NETDOC\_HOST=http://localhost:9742` on the control node for the duration of the tunnel.


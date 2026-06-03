# NetDoc Pro REST API — Testing Guide
<p align="center">
<img width="280" height="566" alt="REST API Activated" src="https://github.com/user-attachments/assets/b9adaefa-d990-4730-a306-922dec418847" />
  <img width="727" height="565" alt="Aedn_Tech_Topology" src="https://github.com/user-attachments/assets/77ec507d-a973-4cdd-bab6-0b18076d5b49" />
</p>

## Prerequisites

1. **Business tier licence** activated
2. **API server enabled** — open the API menu in the top toolbar and enable the REST API toggle. The status bar at the bottom shows `:9742 API` when active.
3. **Bearer token** — copy it from the API menu. You will use this in every request.

---

## 1. Verify the Server is Running

In PowerShell:

```powershell
Invoke-RestMethod http://localhost:9742/health
```

**Expected response:**

```json
{ "status": "ok", "service": "NetDoc Pro API", "port": 9742 }
```

If you get a connection refused error — the API toggle is not enabled. If you get a response, proceed.

---

## 2. PowerShell Scripts

Navigate to the scripts folder and set your token:

```powershell
cd C:\Users\WHITTY\claude\netscan\examples\powershell
$env:NETDOC_TOKEN = "your-token-here"
```

Run each script:

```powershell
# List all devices
.\Get-NetDocDevices.ps1

# Search by label, IP, type, model, VLAN, or status
.\Search-NetDocDevices.ps1 -Query "switch"

# Export to CSV
.\Export-NetDocInventory.ps1 -Path ".\inventory.csv"
```

> **If you get `unauthorized`** — the token env var was set before or after the script read it. Set the token and run in the same session. Never wrap the token in extra quotes.
>
> **If you get no output and no error** — the API returned an empty device list. Make sure your diagram has been saved (`Ctrl+S`) before querying.

---

## 3. Python Scripts

From the netscan root directory:

```powershell
cd C:\Users\WHITTY\claude\netscan
$env:NETDOC_TOKEN = "your-token-here"
```

```powershell
# List all devices
python examples\python\list_devices.py

# Export full inventory to CSV
python examples\python\export_inventory.py > inventory.csv

# Ansible dynamic inventory (grouped by type and VLAN)
python examples\python\netdoc_inventory.py
```

`netdoc_inventory.py` produces valid Ansible dynamic inventory format — devices grouped by type and VLAN with full hostvars including `ansible_host`, `type`, `vlan`, `model`, `status`, and `diagName`.

---

## 4. Bash Scripts (WSL only)

WSL2 has its own network namespace and cannot reach Windows `localhost` directly. Get the Windows host IP first:

```bash
export NETDOC_HOST="http://$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):9742"
export NETDOC_TOKEN="your-token-here"
```

Install `jq` if not present:

```bash
sudo apt install jq
```

Run the scripts:

```bash
cd /mnt/c/Users/WHITTY/claude/netscan
chmod +x examples/bash/*.sh

# List all devices
./examples/bash/list_devices.sh

# Search devices
./examples/bash/search_devices.sh cisco
```

---

## 5. Raw curl (PowerShell)

To inspect raw JSON from any endpoint directly:

```powershell
$env:NETDOC_TOKEN = "your-token-here"

# All devices
curl.exe -H "Authorization: Bearer $env:NETDOC_TOKEN" http://localhost:9742/api/v1/devices

# Ansible inventory
curl.exe -H "Authorization: Bearer $env:NETDOC_TOKEN" http://localhost:9742/api/v1/inventory

# All diagrams
curl.exe -H "Authorization: Bearer $env:NETDOC_TOKEN" http://localhost:9742/api/v1/diagrams

# All VLANs
curl.exe -H "Authorization: Bearer $env:NETDOC_TOKEN" http://localhost:9742/api/v1/vlans

# All IPAM entries
curl.exe -H "Authorization: Bearer $env:NETDOC_TOKEN" http://localhost:9742/api/v1/ipam
```

---

## 6. Available Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Server health check — no auth required |
| GET | `/api/v1/devices` | All devices across all diagrams |
| GET | `/api/v1/devices?diagram=<id>` | Devices filtered to one diagram |
| GET | `/api/v1/vlans` | All VLANs across all diagrams |
| GET | `/api/v1/ipam` | All IPAM reservations |
| GET | `/api/v1/diagrams` | List of all saved diagrams |
| GET | `/api/v1/inventory` | Ansible dynamic inventory format |

All endpoints return `application/json`. The API is **read-only**.

---

## 7. Device Response Fields

Each device returned by `/api/v1/devices` contains:

| Field | Description |
|-------|-------------|
| `label` | Device name as shown on the canvas |
| `ip` | IP address |
| `type` | Device type (`Switch`, `Router`, `Firewall`, `Server`, etc.) |
| `vlan` | VLAN tag (empty if not set) |
| `model` | Device model (empty if not set) |
| `status` | `online` / `offline` / `stale` |
| `diagId` | Diagram identifier |
| `diagName` | Diagram name |
| `id` | Node identifier |

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Could not connect` | API server not running | Enable toggle in API menu, check status bar for `:9742 API` |
| `unauthorized` | Wrong or missing token | Copy token fresh from API menu, set env var and run in same session |
| No output, no error | Empty device list | Save your diagram with `Ctrl+S` then retry |
| WSL `Could not connect` | WSL2 network isolation | Use Windows host IP from `/etc/resolv.conf`, not `localhost` |
| `jq: command not found` | jq not installed in WSL | `sudo apt install jq` |
| Path not found (PowerShell) | Wrong working directory | `cd` to the correct folder before running the script |

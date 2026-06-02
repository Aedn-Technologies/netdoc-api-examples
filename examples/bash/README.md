\# Bash examples



Pure `curl` + `jq`. Works from WSL on the Windows host, or via SSH tunnel from Linux/macOS.



NetDoc Pro is a Windows application and the API binds to `127.0.0.1` only. Remote machines cannot reach the API directly. To use these scripts from Linux or macOS, set up an SSH tunnel to the Windows host first:



```bash

ssh -L 9742:localhost:9742 user@windows-host

```



\## Configuration



```bash

export NETDOC\_HOST="http://localhost:9742"

export NETDOC\_TOKEN="your-bearer-token-here"

```



\## Scripts



\- `list\_devices.sh` — fetch all devices

\- `search\_devices.sh` — filter devices client-side by substring



Make executable: `chmod +x \*.sh`


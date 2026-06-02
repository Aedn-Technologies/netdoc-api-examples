\# PowerShell examples



Native PowerShell — works on Windows PowerShell 5.1 and PowerShell 7+.



\## Configuration



Set your bearer token as an environment variable in your PowerShell profile:



```powershell

$env:NETDOC\_TOKEN = "your-bearer-token-here"

```



Or edit the `$Token` variable at the top of each script.



\## Scripts



\- `Get-NetDocDevices.ps1` — fetch and display all devices

\- `Search-NetDocDevices.ps1` — filter devices client-side by substring

\- `Export-NetDocInventory.ps1` — export device list to CSV



Run with: `.\\Get-NetDocDevices.ps1`


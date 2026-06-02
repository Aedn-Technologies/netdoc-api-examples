<#
.SYNOPSIS
    Export the NetDoc Pro device inventory to CSV.
.PARAMETER Path
    Output CSV file path. Defaults to .\netdoc-inventory.csv.
.EXAMPLE
    .\Export-NetDocInventory.ps1 -Path "C:\reports\inventory.csv"
#>

param(
    [string]$Path = ".\netdoc-inventory.csv"
)

$NetdocHost = if ($env:NETDOC_HOST) { $env:NETDOC_HOST } else { "http://localhost:9742" }
$Token      = if ($env:NETDOC_TOKEN) { $env:NETDOC_TOKEN } else { "your-token-here" }

$Headers = @{ Authorization = "Bearer $Token" }

try {
    $Devices = Invoke-RestMethod -Uri "$NetdocHost/api/v1/devices" -Headers $Headers
    $Devices | Select-Object label, ip, type, model, vlan, status, diagName |
        Export-Csv -Path $Path -NoTypeInformation -Encoding UTF8
    Write-Host "Exported $($Devices.Count) device(s) to $Path" -ForegroundColor Green
}
catch {
    Write-Error "Export failed: $_"
    exit 1
}

<#
.SYNOPSIS
    Lists all devices known to NetDoc Pro.
.EXAMPLE
    .\Get-NetDocDevices.ps1
#>

$NetdocHost = if ($env:NETDOC_HOST) { $env:NETDOC_HOST } else { "http://localhost:9742" }
$Token      = if ($env:NETDOC_TOKEN) { $env:NETDOC_TOKEN } else { "your-token-here" }

$Headers = @{ Authorization = "Bearer $Token" }

try {
    $Devices = Invoke-RestMethod -Uri "$NetdocHost/api/v1/devices" -Headers $Headers
    $Devices | Select-Object label, ip, type, model, vlan, status | Format-Table -AutoSize
}
catch {
    Write-Error "Failed to query NetDoc Pro: $_"
    exit 1
}

<#
.SYNOPSIS
    Search devices in NetDoc Pro by label, IP, model, type, VLAN, or status.
.PARAMETER Query
    The search term. Matched case-insensitively against all fields.
.EXAMPLE
    .\Search-NetDocDevices.ps1 -Query "cisco"
.EXAMPLE
    .\Search-NetDocDevices.ps1 -Query "10.0.99"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Query
)

$NetdocHost = if ($env:NETDOC_HOST) { $env:NETDOC_HOST } else { "http://localhost:9742" }
$Token      = if ($env:NETDOC_TOKEN) { $env:NETDOC_TOKEN } else { "your-token-here" }

$Headers = @{ Authorization = "Bearer $Token" }

try {
    $Devices = Invoke-RestMethod -Uri "$NetdocHost/api/v1/devices" -Headers $Headers
    $Results = $Devices | Where-Object {
        $_.label    -match $Query -or
        $_.ip       -match $Query -or
        $_.model    -match $Query -or
        $_.type     -match $Query -or
        $_.vlan     -match $Query -or
        $_.status   -match $Query -or
        $_.diagName -match $Query
    }
    Write-Host "Found $($Results.Count) matching device(s):" -ForegroundColor Green
    $Results | Select-Object label, ip, type, model, vlan, status | Format-Table -AutoSize
}
catch {
    Write-Error "Search failed: $_"
    exit 1
}

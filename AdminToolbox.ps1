#!/usr/bin/env pwsh

# Check PowerShell version
$minVersion = [Version]"7.4.0"
if ($PSVersionTable.PSVersion -lt $minVersion) {
    Write-Error "This script requires PowerShell $minVersion or later. Current version is $($PSVersionTable.PSVersion)."
    exit 1
}

# Function to write log messages
function Write-Log {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message,

        [Parameter(Mandatory = $false)]
        [string]$LogFile = "AdminToolbox.log"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Add-Content -Path $LogFile -Value $logMessage
    Write-Output $logMessage
}

# Function to get a registry key value (local or remote)
function Get-RegistryKeyValue {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Key,

        [Parameter(Mandatory = $true)]
        [string]$ValueName,

        [Parameter(Mandatory = $false)]
        [string]$ComputerName = $env:COMPUTERNAME
    )

    try {
        Write-Log "Attempting to retrieve registry key value: $Key\$ValueName on $ComputerName"
        $regKey = Invoke-Command -ComputerName $ComputerName -ScriptBlock {
            param($Key, $ValueName)
            Get-ItemProperty -Path "Registry::$Key" -Name $ValueName -ErrorAction Stop
        } -ArgumentList $Key, $ValueName
        $value = $regKey.$ValueName
        Write-Log "Registry key value for '$ValueName' retrieved from $ComputerName: $value"
        return $value
    }
    catch {
        Write-Log "Failed to retrieve the registry key value from $ComputerName. Error: $_"
        return $null
    }
}

# Function to check if a version matches a specific value (local or remote)
function Compare-Version {
    param (
        [Parameter(Mandatory = $true)]
        [string]$CurrentVersion,

        [Parameter(Mandatory = $true)]
        [string]$TargetVersion,

        [Parameter(Mandatory = $false)]
        [string]$ComputerName = $env:COMPUTERNAME
    )

    Write-Log "Comparing versions on $ComputerName - Current: $CurrentVersion, Target: $TargetVersion"
    if ($CurrentVersion -eq $TargetVersion) {
        Write-Log "Version matches on $ComputerName: $TargetVersion"
        return $true
    }
    else {
        Write-Log "Version does not match on $ComputerName. Expected: $TargetVersion, but got: $CurrentVersion"
        return $false
    }
}

# Function to read XML files (local or remote)
function Read-XmlFile {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $false)]
        [string]$ComputerName = $env:COMPUTERNAME
    )

    try {
        Write-Log "Attempting to read XML file: $FilePath on $ComputerName"
        $xmlContent = Invoke-Command -ComputerName $ComputerName -ScriptBlock {
            param($FilePath)
            if (-not (Test-Path $FilePath)) {
                throw "The file '$FilePath' does not exist."
            }
            [xml](Get-Content -Path $FilePath -ErrorAction Stop)
        } -ArgumentList $FilePath
        Write-Log "XML file read successfully from $ComputerName: $FilePath"
        return $xmlContent
    }
    catch {
        Write-Log "Failed to read the XML file from $ComputerName. Error: $_"
        return $null
    }
}

# Function to manage remote admin permissions
function Manage-RemoteAdminPermissions {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Username,

        [Parameter(Mandatory = $true)]
        [ValidateSet("Grant", "Revoke")]
        [string]$Action,

        [Parameter(Mandatory = $true)]
        [string]$ComputerName
    )

    try {
        Write-Log "Attempting to $Action admin permissions for $Username on $ComputerName"
        $result = Invoke-Command -ComputerName $ComputerName -ScriptBlock {
            param($Username, $Action)
            $group = [ADSI]"WinNT://$env:COMPUTERNAME/Administrators,group"
            $user = [ADSI]"WinNT://$env:COMPUTERNAME/$Username,user"
            
            if ($Action -eq "Grant") {
                $group.Add($user.Path)
                return "$Username added to Administrators group"
            }
            elseif ($Action -eq "Revoke") {
                $group.Remove($user.Path)
                return "$Username removed from Administrators group"
            }
        } -ArgumentList $Username, $Action
        Write-Log $result
        return $result
    }
    catch {
        $errorMessage = "Failed to $Action admin permissions for $Username on $ComputerName. Error: $_"
        Write-Log $errorMessage
        return $errorMessage
    }
}

# Function to execute a program remotely
function Execute-RemoteProgram {
    param (
        [Parameter(Mandatory = $true)]
        [string]$ProgramPath,

        [Parameter(Mandatory = $false)]
        [string]$Arguments,

        [Parameter(Mandatory = $true)]
        [string]$ComputerName
    )

    try {
        Write-Log "Attempting to execute $ProgramPath on $ComputerName"
        $result = Invoke-Command -ComputerName $ComputerName -ScriptBlock {
            param($ProgramPath, $Arguments)
            $process = Start-Process -FilePath $ProgramPath -ArgumentList $Arguments -PassThru -Wait
            return "Program executed with exit code: $($process.ExitCode)"
        } -ArgumentList $ProgramPath, $Arguments
        Write-Log $result
        return $result
    }
    catch {
        $errorMessage = "Failed to execute $ProgramPath on $ComputerName. Error: $_"
        Write-Log $errorMessage
        return $errorMessage
    }
}

# Function to write XML files (local or remote)
function Write-XmlFile {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [xml]$XmlContent,

        [Parameter(Mandatory = $false)]
        [string]$ComputerName = $env:COMPUTERNAME
    )

    try {
        Write-Log "Attempting to write XML file: $FilePath on $ComputerName"
        Invoke-Command -ComputerName $ComputerName -ScriptBlock {
            param($FilePath, $XmlContent)
            $XmlContent.Save($FilePath)
        } -ArgumentList $FilePath, $XmlContent
        Write-Log "XML file written successfully to $ComputerName: $FilePath"
        return "XML file written successfully."
    }
    catch {
        $errorMessage = "Failed to write the XML file to $ComputerName. Error: $_"
        Write-Log $errorMessage
        return $errorMessage
    }
}

# Function to modify XML files (local or remote)
function Modify-XmlFile {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string]$XPath,

        [Parameter(Mandatory = $true)]
        [string]$NewValue,

        [Parameter(Mandatory = $false)]
        [string]$ComputerName = $env:COMPUTERNAME
    )

    try {
        Write-Log "Attempting to modify XML file: $FilePath on $ComputerName"
        $result = Invoke-Command -ComputerName $ComputerName -ScriptBlock {
            param($FilePath, $XPath, $NewValue)
            $xml = [xml](Get-Content -Path $FilePath)
            $node = $xml.SelectSingleNode($XPath)
            if ($null -ne $node) {
                $node.InnerText = $NewValue
                $xml.Save($FilePath)
                return "XML file modified successfully."
            } else {
                return "XPath not found in the XML file."
            }
        } -ArgumentList $FilePath, $XPath, $NewValue
        Write-Log $result
        return $result
    }
    catch {
        $errorMessage = "Failed to modify the XML file on $ComputerName. Error: $_"
        Write-Log $errorMessage
        return $errorMessage
    }
}

# Main script execution
function Main {
    Write-Log "AdminToolbox is running..."
    # Add your main logic here
    Write-Log "AdminToolbox execution completed."
}

# Run the main script
Main

# AdminToolbox.ps1

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

# Function to get a registry key value
function Get-RegistryKeyValue {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Key,

        [Parameter(Mandatory = $true)]
        [string]$ValueName
    )

    try {
        Write-Log "Attempting to retrieve registry key value: $Key\$ValueName"
        $regKey = Get-ItemProperty -Path "Registry::$Key" -Name $ValueName -ErrorAction Stop
        $value = $regKey.$ValueName
        Write-Log "Registry key value for '$ValueName' retrieved: $value"
        return $value
    }
    catch {
        Write-Log "Failed to retrieve the registry key value. Error: $_"
        return $null
    }
}

# Function to check if a version matches a specific value
function Compare-Version {
    param (
        [Parameter(Mandatory = $true)]
        [string]$CurrentVersion,

        [Parameter(Mandatory = $true)]
        [string]$TargetVersion
    )

    Write-Log "Comparing versions - Current: $CurrentVersion, Target: $TargetVersion"
    if ($CurrentVersion -eq $TargetVersion) {
        Write-Log "Version matches: $TargetVersion"
        return $true
    }
    else {
        Write-Log "Version does not match. Expected: $TargetVersion, but got: $CurrentVersion"
        return $false
    }
}

# Function to read XML files
function Read-XmlFile {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath
    )

    try {
        Write-Log "Attempting to read XML file: $FilePath"
        if (-not (Test-Path $FilePath)) {
            throw "The file '$FilePath' does not exist."
        }

        $xmlContent = [xml](Get-Content -Path $FilePath -ErrorAction Stop)
        Write-Log "XML file read successfully: $FilePath"
        return $xmlContent
    }
    catch {
        Write-Log "Failed to read the XML file. Error: $_"
        return $null
    }
}

# Main script execution
function Main {
    Write-Log "AdminToolbox is running..."

    # Registry key retrieval example
    $registryKey = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    $registryValue = "CurrentBuild"
    $currentBuild = Get-RegistryKeyValue -Key $registryKey -ValueName $registryValue

    # Version check example
    $targetVersion = "19045"
    $versionMatch = Compare-Version -CurrentVersion $currentBuild -TargetVersion $targetVersion
    
    # XML file reading example
    $xmlFilePath = ".\example.xml"
    if (Test-Path $xmlFilePath) {
        $xmlData = Read-XmlFile -FilePath $xmlFilePath
        if ($xmlData) {
            Write-Log "XML file contents:"
            Write-Log $xmlData.OuterXml
        }
    }
    else {
        Write-Log "XML file not found. Skipping XML reading example."
    }

    Write-Log "AdminToolbox execution completed."
}

# Run the main script
Main

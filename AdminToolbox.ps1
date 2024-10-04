# AdminToolbox.ps1

# Function to get a registry key value
function Get-RegistryKeyValue {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Key,

        [Parameter(Mandatory = $true)]
        [string]$ValueName
    )

    try {
        $regKey = Get-ItemProperty -Path "Registry::$Key" -Name $ValueName -ErrorAction Stop
        $value = $regKey.$ValueName
        Write-Output "Registry key value for '$ValueName' retrieved: $value"
        return $value
    }
    catch {
        Write-Error "Failed to retrieve the registry key value. Error: $_"
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

    if ($CurrentVersion -eq $TargetVersion) {
        Write-Output "Version matches: $TargetVersion"
        return $true
    }
    else {
        Write-Output "Version does not match. Expected: $TargetVersion, but got: $CurrentVersion"
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
        if (-not (Test-Path $FilePath)) {
            throw "The file '$FilePath' does not exist."
        }

        $xmlContent = [xml](Get-Content -Path $FilePath -ErrorAction Stop)
        Write-Output "XML file read successfully."
        return $xmlContent
    }
    catch {
        Write-Error "Failed to read the XML file. Error: $_"
        return $null
    }
}

# Main script execution
function Main {
    Write-Output "AdminToolbox is running..."

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
            Write-Output "XML file contents:"
            Write-Output $xmlData.OuterXml
        }
    }
    else {
        Write-Output "XML file not found. Skipping XML reading example."
    }

    Write-Output "AdminToolbox execution completed."
}

# Run the main script
Main

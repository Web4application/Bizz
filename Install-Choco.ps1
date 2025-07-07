# Set environment variables
$env:chocolateyVersion = "1.4.0"
$env:chocolateyDownloadUrl = "https://community.chocolatey.org/chocolatey.1.4.0.nupkg"
$env:chocolateyUseWindowsCompression = "true"
$env:chocolateyIgnoreProxy = "true"

# Set PowerShell execution policy
Set-ExecutionPolicy Bypass -Scope Process -Force

# Ensure TLS 1.2 is used
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# Run the Chocolatey install script
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Verify installation
choco -v

# Optional: Customize environment variables
$env:chocolateyVersion = "1.4.0"
$env:chocolateyIgnoreProxy = "true"
$env:chocolateyUseWindowsCompression = "true"

# Set PowerShell execution policy
Set-ExecutionPolicy Bypass -Scope Process -Force

# Ensure TLS 1.2 for secure downloads
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# Install Chocolatey
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Refresh session (optional if run interactively)
refreshenv

# Install Dev Tools
choco install git -y
choco install vscode -y
choco install nodejs -y

# Optional: Verify installations
git --version
node --version
code --version

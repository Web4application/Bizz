# --- Environment Setup ---
$env:chocolateyVersion = "1.4.0"
$env:chocolateyIgnoreProxy = "true"
$env:chocolateyUseWindowsCompression = "true"

Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# --- Install Chocolatey ---
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# --- Refresh Environment ---
refreshenv

# --- Install Core Developer Tools ---
choco install git vscode nodejs python docker-desktop postman googlechrome -y

# --- VS Code Extensions ---
$extensions = @(
    "ms-python.python",
    "ms-vscode.vscode-typescript-next",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "github.copilot",
    "ms-azuretools.vscode-docker"
)
foreach ($ext in $extensions) {
    code --install-extension $ext
}

# --- Python Virtual Environment Setup ---
python -m venv DevEnv
.\DevEnv\Scripts\activate
pip install --upgrade pip
pip install flask requests numpy pandas jupyter

# --- Node Global Packages ---
npm install -g typescript eslint prettier nodemon

# --- Git Setup ---
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git init DevProject
Set-Location DevProject
echo "# DevProject" > README.md
git add .
git commit -m "Initial project scaffold"

# --- Docker Init ---
mkdir docker
echo "FROM node:20\nWORKDIR /app\nCOPY . .\nRUN npm install\nCMD [\"npm\", \"start\"]" > docker/Dockerfile

# --- Success Message ---
Write-Host "`n🚀 Full-stack dev environment is installed & configured!" -ForegroundColor Green
Write-Host "📂 You're inside DevProject with Docker, Git, Python, Node.js, and VS Code primed." -ForegroundColor Cyan

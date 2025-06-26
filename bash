# 1. Install if not yet
npm i -D vitest @testing-library/react jsdom

# 2. Run tests
npx vitest

npm i -D vitest @testing-library/react jsdom

# FastAPI example
from fastapi import FastAPI
app = FastAPI()

@app.get(\"/api/assistant/start\")
def start_assistant():
    return {\"message\": \"ProjectPilot AI assistant activated!\"}

# 1) Clone and enter the project
$ git clone https://github.com/Web4application/Bizz.git
$ cd Bizz

# 2) Python deps – create & activate venv
$ python -m venv .venv && source .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt  # or `poetry install`

# 3) Node/TS deps (if package.json exists)
$ npm ci

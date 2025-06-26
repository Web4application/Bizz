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

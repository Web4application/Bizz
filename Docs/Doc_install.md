 ## ⚙️ Installation Guide

Follow these steps to install and run Bizz locally.

---

## Prerequisites

- Python 3.11 (recommended with `pyenv` or `asdf`)
- Node.js ≥ 20 & npm ≥ 10
- Poetry (for Python dep management)
- Docker 24 (for full container support)

---

## Clone and Install

```bash
# Clone the repo
$ git clone https://github.com/Web4application/Bizz.git
$ cd Bizz

# Setup Python backend
$ poetry install
$ poetry run uvicorn main_api:app --reload

# Setup React UI
$ cd lib/ui
$ npm install && npm run dev
```

---

## Docker Alternative

```bash
# Build and run the stack
$ docker compose up --build
```

- Access API: [http://localhost:8000](http://localhost:8000)
- Access UI: [http://localhost:3000](http://localhost:3000)


# 🧪 Bizz CLI Tool

The Bizz CLI (`bizz_cli.py`) provides quick terminal access to AI assistant and file upload features.

---

## Setup

```bash
# Ensure environment variables are set:
export API_URL=http://localhost:8000
export API_KEY=change-me

# Run CLI
python scripts/bizz_cli.py start
```

---

## Commands

### `start`
Ping the assistant and return a welcome message.
```bash
bizz start
```

### `chat --message "..."`
Send a message to the assistant.
```bash
bizz chat --message "What's the weather?"
```

### `upload --file path/to/file.txt`
Upload a file (e.g. JSON or TXT).
```bash
bizz upload --file ./notes.txt
```

---

## Notes
- This CLI can be packaged via `poetry` or used directly.
- Output includes memory, assistant replies, and status feedback.
- Easily scriptable into automation or cron jobs.


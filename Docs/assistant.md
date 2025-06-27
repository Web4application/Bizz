# 🧠 Assistant API

The Bizz AI Assistant is a REST API designed to emulate chat behavior with optional memory persistence.

---

## Endpoints

### `GET /api/assistant/start`

> Used to ping and initialize the assistant system.

```bash
curl http://localhost:8000/api/assistant/start
```

Returns:

```json
{ "message": "ProjectPilot AI assistant activated!" }
```

---

### `POST /api/assistant/chat`

**Secure** – Requires `X-API-Key` header

Send user messages to the assistant:

```bash
curl -X POST http://localhost:8000/api/assistant/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{ "message": "Hello" }'
```

Returns the assistant's response and memory:

```json
{
  "response": "You said: Hello",
  "memory": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "You said: Hello" }
  ]
}
```

---

## Notes

- The memory buffer is in-memory only and limited to the last 50 messages.
- To persist data long-term, consider integrating Redis, PostgreSQL, or vector DBs.


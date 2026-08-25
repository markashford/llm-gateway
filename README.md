# LLM Gateway

Unified FastAPI gateway for calling multiple LLM providers, with a Redis token-bucket rate limiter that stays consistent across processes.

## Features

- Groq chat completions, with a provider interface ready for OpenAI, Anthropic, and Google
- Distributed rate limiting via Redis + Lua
- Environment-based configuration through Pydantic Settings
- Docker Compose for local Redis + API

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/docs

Without Docker:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# start Redis, then:
uvicorn app.api.main:app --reload --port 8000
```

## Chat

`POST /chat`

```json
{
  "provider": "groq",
  "model": "llama-3.1-8b-instant",
  "messages": [{"role": "user", "content": "Hello!"}],
  "temperature": 0.7,
  "max_tokens": 25
}
```

Other routes:

- `GET /health`
- `GET /providers`

Rate-limited requests return `429` with a `Retry-After` header.

## Tests

```bash
pytest
```

## License

MIT

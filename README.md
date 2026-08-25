# Tapistro System Design

## Overview

This project demonstrates a clean, extensible architecture for calling multiple Large Language Model (LLM) providers via a unified API, with a distributed rate limiter that works across processes and servers. The solution is built using FastAPI, Redis, and Pydantic, and is designed for production-readiness, scalability, and maintainability.

## Features

- **LLM Provider:**
  The API currently supports Groq, with placeholders for OpenAI, Anthropic, and Google.
- **Distributed Rate Limiting:**  
  Implements a token bucket algorithm using Redis and Lua scripting, ensuring consistent rate limiting across multiple backend instances.
- **Clean Architecture:**  
  Separation of concerns between API, middleware, provider logic, and configuration.
- **Environment-based Configuration:**  
  All secrets and settings are loaded from environment variables or `.env` files.
- **Docker & Compose Support:**  
  Ready for local development and deployment with Docker and Docker Compose.

## Design Decisions

- **Groq as Initial Provider:**  
  Groq is implemented as the initial provider due to its competitive pricing and performance. Other providers can be added similarly.
- **Rate Limiting:**  
  The token bucket algorithm is implemented in Redis using Lua for atomicity and performance. This avoids race conditions and ensures distributed consistency.
- **Configuration:**  
  Uses Pydantic Settings for type-safe, environment-driven configuration.
- **Error Handling:**  
  API returns clear error messages for unknown providers and rate limit violations.
- **Extensibility:**  
  Adding a new provider requires only implementing the `LLMClient` interface and updating the provider router.

## Trade-offs Considered

- **Redis as a Single Point of Failure:**  
  While Redis is fast and reliable, it introduces a dependency. For high availability, Redis clustering or managed Redis is recommended.
- **Synchronous Lua Scripts:**  
  Lua scripts are fast but may block Redis under heavy load. For extreme scale, consider sharding or alternative rate limiting strategies.
- **Minimal Provider Implementations:**  
  Only Groq is fully implemented for brevity. Others can be added following the same pattern.

## Project Structure

```
app/
  api/                # FastAPI entrypoint
  core/               # Configuration and types
  middleware/         # Rate limiting middleware
  providers/          # Provider interfaces and implementations
  rate_limiter/       # Redis token bucket implementation
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## Running Locally

1. **Clone the repository**
2. **Set up your `.env` file** (see `.env.example`)
3. **Build and start services:**
   ```sh
   docker-compose up --build
   ```
4. **Access the API docs:**  
   [http://localhost:8000/docs](http://localhost:8000/docs)

## API Usage

- **POST `/chat`**
  ```json
  {
    "provider": "groq",
    "model": "llama-3.1-8b-instant",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 25
  }
  ```

## Rate Limiting

- Each request is rate limited per tenant and route using a distributed token bucket in Redis.
- If the limit is exceeded, a `429 Too Many Requests` response is returned with a `Retry-After` header.

## Adding Providers

1. Add your provider to `get_providers()` in `app/providers/router.py`.

## Testing

- Unit tests can be added using `pytest` and `pytest-asyncio`.
- To run tests:
  ```sh
  pytest
  ```

## Further Improvements

- Add more provider implementations.
- Implement provider-specific rate limits.
- Add authentication and logging.
- Expand unit and integration test coverage.

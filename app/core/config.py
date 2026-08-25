from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    groq_api_key: str | None = None
    
    redis_url: str = "redis://localhost:6379/0"
    
    rl_rate: int = 5          # Default rate limit (requests per second)
    rl_burst_size: int = 10    # Default burst size

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()

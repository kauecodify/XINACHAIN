"""Configuration settings for XINACHAIN."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # LLM Configuration
    llm_model: str = "gpt-oss:20b"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "dummy"
    
    # External API Configuration
    exchange_rate_api: str = "https://api.exchangerate-api.com/v4"
    weather_api: str = "https://api.openweathermap.org/data/2.5"
    weather_api_key: str = ""
    
    # Default values
    default_exchange_rate_usd_brl: float = 5.0
    default_exchange_rate_usd_cny: float = 7.0
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

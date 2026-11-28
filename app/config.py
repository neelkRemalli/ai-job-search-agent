import os

from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr


DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"

# Populate os.environ from the project's local dotenv file.
load_dotenv()


class Settings(BaseModel):
    """Validated runtime settings, with API keys masked as secrets."""

    groq_api_key: SecretStr
    tavily_api_key: SecretStr
    groq_model: str = DEFAULT_GROQ_MODEL


def get_settings() -> Settings:
    """Build settings from environment variables and reject missing API keys."""

    values = {
        "groq_api_key": os.environ.get("GROQ_API_KEY"),
        "tavily_api_key": os.environ.get("TAVILY_API_KEY"),
        "groq_model": os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL),
    }

    missing = [
        env_name
        for env_name, value in (
            ("GROQ_API_KEY", values["groq_api_key"]),
            ("TAVILY_API_KEY", values["tavily_api_key"]),
        )
        if not value
    ]

    if missing:
        raise ValueError(
            f"Required environment variable(s) missing: {', '.join(missing)}"
        )

    return Settings(**values)

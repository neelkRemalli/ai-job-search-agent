import os
import unittest
from unittest.mock import patch

from app.config import DEFAULT_GROQ_MODEL, get_settings


class GetSettingsTests(unittest.TestCase):
    def test_returns_settings_when_both_api_keys_are_provided(self):
        environment = {
            "GROQ_API_KEY": "test-groq-key",
            "TAVILY_API_KEY": "test-tavily-key",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = get_settings()

        self.assertEqual(settings.groq_api_key.get_secret_value(), "test-groq-key")
        self.assertEqual(settings.tavily_api_key.get_secret_value(), "test-tavily-key")

    def test_uses_default_model_when_groq_model_is_absent(self):
        environment = {
            "GROQ_API_KEY": "test-groq-key",
            "TAVILY_API_KEY": "test-tavily-key",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = get_settings()

        self.assertEqual(settings.groq_model, "openai/gpt-oss-20b")
        self.assertEqual(settings.groq_model, DEFAULT_GROQ_MODEL)

    def test_accepts_custom_groq_model(self):
        environment = {
            "GROQ_API_KEY": "test-groq-key",
            "TAVILY_API_KEY": "test-tavily-key",
            "GROQ_MODEL": "custom/model",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = get_settings()

        self.assertEqual(settings.groq_model, "custom/model")

    def test_reports_both_missing_api_keys(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                get_settings()

        message = str(context.exception)
        self.assertIn("GROQ_API_KEY", message)
        self.assertIn("TAVILY_API_KEY", message)


if __name__ == "__main__":
    unittest.main()

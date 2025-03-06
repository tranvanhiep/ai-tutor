import os

from crewai import LLM

from utils import load_env


class Config:
    """Centralized configuration for LLM and memory setting."""
    def __init__(self):
        load_env()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL")
        self.gemini_embedder_model = os.getenv("GEMINI_EMBEDDER_MODEL")

    def get_gemini_llm(self):
        if self.gemini_api_key is None:
            raise ValueError("GEMINI_API_KEY is not set")
        if self.gemini_model is None:
            raise ValueError("GEMINI_MODEL is not set")

        return LLM(
            model=self.gemini_model,
            api_key=self.gemini_api_key,
            temperature=1.0,
        )

    def get_openai_llm(self):
        if self.openai_api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        if self.openai_model is None:
            raise ValueError("OPENAI_MODEL is not set")

        return LLM(
            model=self.openai_model,
            api_key=self.openai_api_key,
            temperature=1.0,
       )

    def get_google_embedder(self):
        if self.gemini_api_key is None and self.gemini_embedder_model is None:
            return None
        else:
            if self.gemini_api_key is None:
                raise ValueError("GEMINI_API_KEY is not set")
            if self.gemini_embedder_model is None:
                raise ValueError("GEMINI_EMBEDDER_MODEL is not set")

        return {
            "provider": "google",
            "config": {
                "api_key": self.gemini_api_key,
                "model": self.gemini_embedder_model,
            },
        }

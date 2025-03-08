import os

from crewai import LLM

from utils.load_env import load_env


class Config:
    """Centralized configuration for LLM and memory setting."""
    def __init__(self):
        load_env()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_model = os.getenv("GOOGLE_MODEL")
        self.google_embedder_model = os.getenv("GOOGLE_EMBEDDER_MODEL")
        self.local_model = os.getenv("LOCAL_MODEL")

    def get_google_llm(self):
        if self.google_api_key is None:
            raise ValueError("GOOGLE_API_KEY is not set")
        if self.google_model is None:
            raise ValueError("GOOGLE_MODEL is not set")

        return LLM(
            model=self.google_model,
            api_key=self.google_api_key,
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
        if self.google_api_key is None and self.google_embedder_model is None:
            return None
        else:
            if self.google_api_key is None:
                raise ValueError("GOOGLE_API_KEY is not set")
            if self.google_embedder_model is None:
                raise ValueError("GOOGLE_EMBEDDER_MODEL is not set")

        return {
            "provider": "google",
            "config": {
                "api_key": self.google_api_key,
                "model": self.google_embedder_model,
            },
        }

    def get_local_llm(self):
        if self.local_model is None:
            raise ValueError("LOCAL_MODEL is not set")

        return LLM(
            model=self.local_model,
            base_url="http://localhost:11434",
            temperature=1.0,
        )

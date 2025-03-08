from enum import Enum


class LLMType(Enum):
    """Enum for different types of Large Language Models."""

    GOOGLE = "google"
    OPENAI = "openai"
    LOCAL = "local"

    def __str__(self) -> str:
        """Return the value of the enum."""
        return self.value

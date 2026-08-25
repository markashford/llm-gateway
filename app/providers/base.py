import abc
from app.core.types import LLMRequest, LLMResponse


class LLMClient(abc.ABC):
    """Abstract base class for all LLM provider clients."""

    @abc.abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Send a completion request to the provider."""
        raise NotImplementedError

from abc import ABC, abstractmethod

import httpx


class LLMProvider(ABC):
    @abstractmethod
    def chat(self, messages: list[dict[str, str]]) -> str:
        """Send chat history, return the assistant's reply text."""


class LLMUnavailableError(Exception):
    pass


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str = "llama3.2:1b",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ):
        self.model = model
        self.base_url = base_url
        self.timeout = timeout

    def chat(self, messages: list[dict[str, str]]) -> str:
        url = f"{self.base_url}/api/chat"

        payload = {"model": self.model, "messages": messages, "stream": False}

        try:
            response = httpx.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()

        except httpx.ConnectError as e:
            raise LLMUnavailableError(
                "Cannot connect to Ollama. Make sure the Ollama server is running."
            ) from e

        except httpx.TimeoutException as e:
            raise LLMUnavailableError(
                f"Ollama request timed out after {self.timeout} seconds."
            ) from e

        except httpx.HTTPStatusError as e:
            raise LLMUnavailableError(
                f"Ollama returned HTTP {e.response.status_code}. "
                f"Check whether model '{self.model}' is installed and available."
            ) from e

        data = response.json()
        return data["message"]["content"]


if __name__ == "__main__":
    provider = OllamaProvider()
    print(provider.chat([{"role": "user", "content": "Say hello in 5 words."}]))

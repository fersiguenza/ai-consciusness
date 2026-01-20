import yaml
import os

from typing import Any, Optional


class Config:
    """Configuration loader for the RegretGraph system."""
    def __init__(self, path: str = 'config.yaml') -> None:
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)

    @property
    def llm_provider(self) -> str:
        return self.get('llm_provider', 'ollama')

    @property
    def model(self) -> str:
        return self.get('model', 'llama2')

    @property
    def openai_api_key(self) -> Optional[str]:
        return self.get('openai_api_key', os.getenv('OPENAI_API_KEY'))

    @property
    def bedrock_region(self) -> str:
        return self.get('bedrock_region', 'us-east-1')

    @property
    def bedrock_model_id(self) -> str:
        return self.get('bedrock_model_id', 'anthropic.claude-v2')

    @property
    def regret_threshold(self) -> int:
        return self.get('regret_threshold', 7)

    @property
    def forgetting_decay(self) -> int:
        return self.get('forgetting_decay', 1)

    @property
    def mood_threshold(self) -> int:
        return self.get('mood_threshold', 5)

    @property
    def ollama_url(self) -> str:
        return os.getenv('OLLAMA_URL') or self.get('ollama_url', 'http://localhost:11434/api/generate')

    def create_llm_provider(self):
        """Create and return the appropriate LLM provider based on configuration."""
        from .llm_module import OllamaProvider, OpenAIProvider, BedrockProvider

        provider_type = self.llm_provider.lower()

        if provider_type == 'ollama':
            return OllamaProvider(self.ollama_url, self.model)
        elif provider_type == 'openai':
            if not self.openai_api_key:
                raise ValueError("OpenAI API key required for OpenAI provider")
            return OpenAIProvider(self.openai_api_key, self.model)
        elif provider_type == 'bedrock':
            return BedrockProvider(self.bedrock_region, self.bedrock_model_id)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}")

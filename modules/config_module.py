import yaml

from typing import Any, Optional


class Config:
    """Configuration loader for the consciousness proxy."""
    def __init__(self, path: str = 'config.yaml') -> None:
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)

    @property
    def model(self) -> str:
        return self.get('model', 'llama2')

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
        return self.get('ollama_url', 'http://localhost:11434/api/generate')

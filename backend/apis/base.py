# possible base calss for data consistency between multiple apis

from abc import ABC, abstractmethod
from typing import Any


class DataSourceAdapter(ABC):
    """Shared contract for data-collection API adapters."""

    @abstractmethod
    def fetch(self, raw_input: Any) -> Any:
        """Fetch data from the source; return normalized output (e.g. dict/list)."""
        pass

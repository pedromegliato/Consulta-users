import random
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    attempts: int = 3
    base_delay_seconds: float = 0.2
    max_delay_seconds: float = 2.0

    def delay_for(self, attempt: int, retry_after_seconds: float | None = None) -> float:
        if retry_after_seconds is not None:
            return min(retry_after_seconds, self.max_delay_seconds)
        exponential = self.base_delay_seconds * 2.0 ** (attempt - 1)
        return min(exponential, self.max_delay_seconds) * random.uniform(0.5, 1.0)

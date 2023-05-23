import asyncio
import random
from datetime import timedelta

class RetryPolicy:
    def __init__(
        self,
        initial_interval: timedelta,
        backoff_coefficient: int,
        maximum_interval: timedelta,
        maximum_attempts: int,
        non_retryable_errors: set[Exception],
    ):
        self.initial_interval = initial_interval
        self.backoff_coefficient = backoff_coefficient
        self.maximum_interval = maximum_interval
        self.maximum_attempts = maximum_attempts
        self.non_retryable_errors = non_retryable_errors

async def retry_with_backoff(func, *args, retry_policy: RetryPolicy, **kwargs):
    attempts = 0
    interval_seconds = retry_policy.initial_interval.total_seconds()
    while attempts < retry_policy.maximum_attempts:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            attempts += 1
            if (
                attempts >= retry_policy.maximum_attempts
                or type(e) in retry_policy.non_retryable_errors
            ):
                raise
            backoff_time = interval_seconds * (
                retry_policy.backoff_coefficient ** (attempts - 1)
            )
            backoff_time = min(
                backoff_time, retry_policy.maximum_interval.total_seconds()
            )
            backoff_time = random.uniform(0.5 * backoff_time, 1.5 * backoff_time)
            print(f"Retrying after {backoff_time:.2f} seconds...")
            await asyncio.sleep(backoff_time)
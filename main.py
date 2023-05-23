import asyncio
from my_dataclass import ComposeGreetingInput
from my_workflow import retry_with_backoff, RetryPolicy

from datetime import timedelta

from activities import compose_greeting, compose_new_greeting

async def greeting_workflow(name: str) -> str:
    greeting_input = ComposeGreetingInput("Hello", name)
    farewell_input = ComposeGreetingInput("Goodbye", name)
    retry_policy = RetryPolicy(
        initial_interval=timedelta(seconds=1),
        backoff_coefficient=1,
        maximum_interval=timedelta.max,
        maximum_attempts=float("inf"),
        non_retryable_errors=set(),
    )

    greeting_function = await retry_with_backoff(
        compose_greeting,
        greeting_input,
        retry_policy=retry_policy,
    )
    farewell_function = await retry_with_backoff(
        compose_new_greeting,
        farewell_input,
        retry_policy=retry_policy,
    )
    return greeting_function, farewell_function

async def main():
    try:
        result = await greeting_workflow("World")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
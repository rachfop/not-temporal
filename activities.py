from my_dataclass import ComposeGreetingInput

import random

import asyncio


async def compose_greeting(input: ComposeGreetingInput) -> str:
    if random.random() < 0.8:
        raise RuntimeError("Intentional failure")
    return f"{input.greeting}, {input.name}!"


async def compose_new_greeting(input: ComposeGreetingInput) -> str:
    attempts = 0
    while attempts < 4:
        await asyncio.sleep(1)
        attempts += 1
        print(f"Attempt {attempts} of 4")
    return f"{input.greeting}, {input.name}!"

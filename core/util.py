import asyncio


def snake_to_camel(name: str) -> str:
    """Convert snake case to camel case."""
    return "".join([i.capitalize() for i in name.split("_")])


async def nop():
    """just a nop"""
    await asyncio.sleep(0)

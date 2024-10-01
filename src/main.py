import asyncio

from src.infrastructure.cli.app import cli


async def main() -> None:
    cli()

if __name__ == "__main__":
    asyncio.run(main())

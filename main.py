import asyncio
from bot.app import create_app


def main():
    asyncio.run(create_app())


if __name__ == "__main__":
    main()

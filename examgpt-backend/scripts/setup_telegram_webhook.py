import asyncio

import telegram
from lib.utils import get_api_url, get_env, load_env_files


async def set_webhook():
    load_env_files()
    bot_token = get_env("TG_BOT_TOKEN")
    stage = get_env("STAGE")
    region = get_env("REGION")

    api_gateway_url = get_api_url("chat", stage, region)
    print(f"{api_gateway_url=}")

    bot = telegram.Bot(token=bot_token)
    response = await bot.set_webhook(url=api_gateway_url)

    if not response:
        raise Exception("Could not set webhook url")
    else:
        print(f"Webhook set to: {api_gateway_url}")


if __name__ == "__main__":
    asyncio.run(set_webhook())

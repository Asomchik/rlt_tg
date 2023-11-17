"""
Main module. Starts TG Bot. Handling request-response with users
"""
import asyncio
import os

from telethon.sync import TelegramClient
from telethon import events

from dotenv import load_dotenv
from query_handler import aggregate_payments


# Fetch necessary environment variables
load_dotenv()
token = os.getenv('TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Initialize Telegram client
client = TelegramClient('rlt_bot', api_id=int(api_id), api_hash=api_hash).start(bot_token=token)


@client.on(events.NewMessage)
async def rlt_bot_aggregator(event):
    """Event handler for new messages"""
    if event.is_private:
        message_text = event.text
        response_text = await aggregate_payments(message_text)
        await event.respond(response_text)


async def main():
    """Define the main asynchronous function"""
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

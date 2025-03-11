import asyncio
import logging
from pyrogram import Client, filters
from scraper import TwitterScraper

API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("TwitterDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
scraper = TwitterScraper()

logging.basicConfig(level=logging.INFO)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send /download <username> to fetch all tweets from a Twitter/X account.")

@app.on_message(filters.command("download"))
async def download_tweets(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /download <username>")
        return
    
    username = message.command[1]
    await message.reply_text(f"Fetching tweets from @{username}...")

    tweets = await scraper.get_tweets(username)
    
    if not tweets:
        await message.reply_text("No tweets found or account is private.")
        return

    for tweet in tweets:
        caption = f"📝 {tweet['text']}\n🔗 {tweet['url']}"
        if tweet["media"]:
            await client.send_photo(chat_id=message.chat.id, photo=tweet["media"], caption=caption)
        else:
            await message.reply_text(caption)

app.run()

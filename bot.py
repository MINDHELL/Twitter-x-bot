import asyncio
import logging
from pyrogram import Client, filters
from scraper import TwitterScraper

API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7888029778:AAHeC7P5zONGjN3mY5q0Rm6-V1zzPx1ywEQ"

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

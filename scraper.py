import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class TwitterScraper:
    async def get_tweets(self, username):
        url = f"https://twitter.com/{username}"
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await asyncio.sleep(5)

            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        tweets = []

        for tweet in soup.find_all("article"):
            text = tweet.get_text()
            tweet_url = tweet.find("a", href=True)
            tweet_media = tweet.find("img")

            media_url = tweet_media["src"] if tweet_media else None
            tweet_link = f"https://twitter.com{tweet_url['href']}" if tweet_url else None

            tweets.append({"text": text, "url": tweet_link, "media": media_url})

        return tweets

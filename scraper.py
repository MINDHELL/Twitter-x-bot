from playwright.async_api import async_playwright

async def get_tweets(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(f"https://twitter.com/{username}")
            await page.wait_for_selector("article")  # Ensure tweets are loaded
            tweets = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll("article")).map(tweet => tweet.innerText);
            }''')
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            tweets = []
        
        await browser.close()
        return tweets

import asyncio
from playwright.async_api import async_playwright, Playwright

async def run(playwright: Playwright):
    webkit = playwright.webkit
    browser = await webkit.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://dns.ru")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())

# 1729203798450/Ec2vRWuhVlUJjqao/KjZA7qLlOoIuun8lEH2boA==
# 1729203797909/fMqw5PDPSwJ4Be12/kyOdfsCrL6GXYZl/TXpRsQ==

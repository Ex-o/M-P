from bs4 import BeautifulSoup
import json

import asyncio
from playwright.async_api import async_playwright


async def get_ll_from_yandex_url(url):
    p = await async_playwright().start()
    for browser_type in [p.chromium]:
        browser = await browser_type.launch()
        page = await browser.new_page()
        await page.goto(url)
        bs = BeautifulSoup(await page.content(), features="html.parser")
        test = bs.find("script", {"class": "state-view"}).next
        js = json.loads(test)
        return js['map']['location']['center']

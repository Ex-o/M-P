import requests
from bs4 import BeautifulSoup
import json

from playwright.sync_api import sync_playwright


def get_ll_from_yandex_url(url):
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            browser = browser_type.launch()
            page = browser.new_page()
            page.goto(url)
            bs = BeautifulSoup(page.content(), features="html.parser")
            test = bs.find("script", {"class": "state-view"}).next
            js = json.loads(test)
            return js['map']['location']['center']

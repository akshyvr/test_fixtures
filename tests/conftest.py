import pytest
from playwright.sync_api import sync_playwright
from pathlib import  Path

@pytest.fixture
def context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        yield context

        browser.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page

@pytest.mark.usefixtures()
def goto(url,page):
    page.goto(url)

import sys
import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
#
# Ensure project root (one level above tests/) is on sys.path so imports like 'pages.*' work
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

@pytest.fixture
def context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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

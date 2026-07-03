from playwright.sync_api import Page

class Login_page:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str):
        # navigate is expected to be done by test
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Submit").click()

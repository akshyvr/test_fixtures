from playwright.sync_api import Page

class TopDeals_page:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_load_state(self):
        self.page.wait_for_load_state()

    def search(self, text: str):
        self.page.get_by_label("Search:").fill("")
        self.page.get_by_label("Search:").type(text)

    def first_row_text(self):
        name = self.page.locator("(//tr/td[1])[1]").text_content()
        price = self.page.locator("(//tr/td[2])[1]").text_content()
        discount_price = self.page.locator("(//tr/td[3])[1]").text_content()
        return name, price, discount_price

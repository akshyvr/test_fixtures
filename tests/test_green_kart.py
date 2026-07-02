from playwright.sync_api import Page

class Products_page:

    vegetable_name_locator = "//h4"

    def __init__(self, page: Page):
        self.page = page


    def select_vegetable(self, name: str, quantity: int):

        vegetables = self.page.locator(self.vegetable_name_locator)

        for i in range(vegetables.count()):

            vegetable_name = vegetables.nth(i).text_content().split("-")[0].strip()

            if vegetable_name == name:

                quantity_input = self.page.locator(
                    f"(//input[@type='number'])[{i+1}]"
                )

                current_quantity = int(quantity_input.input_value())

                while current_quantity < quantity:
                    self.page.locator(
                        f"(//a[contains(@class,'increment')])[{i+1}]"
                    ).click()
                    current_quantity += 1

                self.page.locator(
                    f"(//button[contains(text(),'ADD TO CART')])[{i+1}]"
                ).click()

                break

    def select_vegetables(self, products: dict):
        for vegetable_name, quantity in products.items():
            self.select_vegetable(vegetable_name, quantity)
    def goto_cart(self):
        self.page.get_by_alt_text("Cart").click()

    def click_button(self, button_name):
        self.page.get_by_role("button", name=button_name).click()

    def select(self, value):
        self.page.get_by_role("combobox").select_option(value)

    def click_checkbox(self, locator):
        self.page.locator(locator).check()
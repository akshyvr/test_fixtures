from playwright.sync_api import Page
import re

class Flite_page:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_load_state(self):
        self.page.wait_for_load_state()

    def select_round_trip_if_present(self):
        options = self.page.locator("//*[@id='ctl00_mainContent_rbtnl_Trip']/tbody/tr/td/label")
        for i in range(options.count()):
            if options.nth(i).inner_text().strip() == "Round Trip":
                self.page.locator("//*[@name='ctl00$mainContent$rbtnl_Trip']").nth(i).click()
                break

    def select_origin(self, value: str):
        self.page.locator("#ctl00_mainContent_ddl_originStation1_CTXTaction").click()
        self.page.locator(f"//a[@value='{value}']").click()

    def select_destination(self, value: str):
        # second occurrence often is the 2nd matching element
        self.page.locator(f"(//a[@value='{value}'])[2]").click()

    def select_date(self, day: str, occurrence: int = 1):
        # occurrence selects which matching day (1-based index)
        self.page.locator(f"(//a[normalize-space()='{day}'])[{occurrence}]").click()

    def open_return_date_picker(self):
        self.page.locator("#ctl00_mainContent_view_date2").click()

    def set_passengers(self, adults: int = 1, children: int = 0):
        self.page.locator("#divpaxinfo").click()
        # clicks increase counts from default 1 adult
        for i in range(max(0, adults - 1)):
            self.page.locator("//div[@id='divAdult']/div[2]/span[3]").click()
        for i in range(max(0, children)):
            self.page.locator("#hrefIncChd").click()
        self.page.locator("#divpaxinfo").click()

    def select_currency(self, value: str):
        self.page.locator("#ctl00_mainContent_DropDownListCurrency").select_option(value=value)

    def apply_discount(self, discount_text: str):
        discount = self.page.locator("//*[@id='discount-checkbox']/div/label")
        for i in range(discount.count()):
            if discount.nth(i).text_content().strip() == discount_text:
                discount.nth(i).click(force=True)
                break

    # --- Query helpers for assertions -------------------------------------------------
    def get_passenger_counts(self):
        """Parse and return (adults, children) from the passenger summary text."""
        text = self.page.locator("#divpaxinfo").text_content().strip()
        adults = 1
        children = 0
        m_adult = re.search(r"(\d+)\s*Adult", text)
        m_child = re.search(r"(\d+)\s*Child", text)
        if m_adult:
            adults = int(m_adult.group(1))
        if m_child:
            children = int(m_child.group(1))
        return adults, children

    def get_selected_currency(self):
        """Return the selected currency value from the dropdown."""
        return self.page.locator("#ctl00_mainContent_DropDownListCurrency").input_value()

    def is_discount_applied(self, discount_text: str) -> bool:
        """Return True if the checkbox for the given discount label is checked.

        Tries several DOM relationships to accommodate different markup patterns.
        """
        label_locator = self.page.locator(f"//*[@id='discount-checkbox']//label[normalize-space()=\"{discount_text}\"]")
        if label_locator.count() == 0:
            return False

        # try several common relationships to find the input element
        xpath_candidates = [
            'preceding-sibling::input',
            'following-sibling::input',
            './/input',
            'ancestor::label//input',
            'parent::*/input',
        ]
        for xp in xpath_candidates:
            try:
                chk = label_locator.locator(xp)
                if chk.count() and chk.first.is_checked():
                    return True
            except Exception:
                continue

        # try 'for' attribute on label -> input id
        try:
            for_attr = label_locator.get_attribute('for')
            if for_attr:
                input_locator = self.page.locator(f"#{for_attr}")
                if input_locator.count() and input_locator.first.is_checked():
                    return True
        except Exception:
            pass

        # fallback: inspect attributes on the label
        class_attr = label_locator.get_attribute('class') or ''
        aria_checked = label_locator.get_attribute('aria-checked') or ''
        return 'checked' in class_attr.lower() or aria_checked.lower() == 'true'
    def get_passenges_selected_details(self):
        return self.page.locator("#divpaxinfo").text_content()
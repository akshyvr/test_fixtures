import random
import time
import re
import pytest
from playwright.sync_api import expect

from test_green_kart import Products_page
testdata_for_search = ["banana", "strawberry", "potato", "cherry"]
def test_e2e(page):
    products_page = Products_page(page)

    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/")

    products_page.select_vegetables({"Banana": 2,"Tomato": 3, "Beans": 1})
    products_page.goto_cart()
    products_page.click_button("PROCEED TO CHECKOUT")
    products_page.click_button("Place Order")
    products_page.select("Brazil")
    products_page.click_checkbox(".chkAgree")
    products_page.click_button("Proceed")

def test_flite_booking_page(page, context):
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/")
    with context.expect_page() as new_page:
        page.get_by_text("Flight Booking").click()
    flite_page = new_page.value
    flite_page.wait_for_load_state()
    expect(flite_page).to_have_title('QAClickJet - Flight Booking for Domestic and International, Cheap Air Tickets')
    return flite_page

def testflite_page_functionals(page,context):
    flite_page = test_flite_booking_page(page, context)
    options = flite_page.locator("//*[@id='ctl00_mainContent_rbtnl_Trip']/tbody/tr/td/label").count()
    for i in range(options):
        print(flite_page.locator("//*[@id='ctl00_mainContent_rbtnl_Trip']/tbody/tr/td/label").nth(i).inner_text().strip())
        if flite_page.locator("//*[@id='ctl00_mainContent_rbtnl_Trip']/tbody/tr/td/label").nth(i).inner_text().strip() == "Round Trip":
            flite_page.locator("//*[@name='ctl00$mainContent$rbtnl_Trip']").nth(i).click()
    time.sleep(4)

def testflite_page_functionals_e2e(page, context):
    flite_page = test_flite_booking_page(page, context)
    # flite_page.locator("//*[@id='ctl00_mainContent_ddl_originStation1_CTXTaction']").click()
    flite_page.locator("#ctl00_mainContent_ddl_originStation1_CTXTaction").click()
    flite_page.locator("//a[@value='BLR']").click()
    flite_page.locator("(//a[@value='GOI'])[2]").click()
    flite_page.locator("(//a[normalize-space()='8'])[1]").click()
    flite_page.locator("#ctl00_mainContent_view_date2").click()
    flite_page.locator("(//a[normalize-space()='12'])[2]").click()
    flite_page.locator("#divpaxinfo").click()
    for i in range(2):
        flite_page.locator("//div[@id='divAdult']/div[2]/span[3]").click()
    for i in range(1):
        flite_page.locator("#hrefIncChd").click()
    flite_page.locator("#divpaxinfo").click()
    flite_page.locator("#ctl00_mainContent_DropDownListCurrency").select_option(value='USD')
    discount = flite_page.locator("//*[@id='discount-checkbox']/div/label")
    print(discount.all_text_contents())
    for i in range(discount.count()):
        if discount.nth(i).text_content().strip() == 'Senior Citizen':
            discount.nth(i).click(force=True)
    time.sleep(5)

def test_topdeals_page_functionals(page, context):
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/")
    with context.expect_page() as new_page:
        page.get_by_text("Top Deals").click()
    top_deals = new_page.value
    top_deals.wait_for_load_state()
    expect(top_deals).to_have_title("GreenKart - veg and fruits kart")
    return  top_deals

def test_topdeals_page_functionals_e2e(page, context):
    search_product = random.choice(testdata_for_search)
    top_deals_page = test_topdeals_page_functionals(page, context)
    top_deals_page.get_by_label("Search:").type(search_product)
    expect(top_deals_page.locator("(//tr/td[1])[1]")).to_contain_text(search_product.capitalize())
    print(f"price of an {top_deals_page.locator("(//tr/td[1])[1]").text_content()} is"
          f" {top_deals_page.locator("(//tr/td[2])[1]").text_content()} and dicsount price"
          f" is {top_deals_page.locator("(//tr/td[3])[1]").text_content()}")






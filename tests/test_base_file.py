import random
import time
import re
import pytest
from playwright.sync_api import expect

from pages.products_page import Products_page
from pages.flite_page import Flite_page
from pages.top_deals_page import TopDeals_page
from pages.login_page import Login_page


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


@pytest.fixture
def flite_page_obj(page, context):
    """Open Flight Booking popup and return Flite_page POM instance."""
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/")
    with context.expect_page() as new_page:
        page.get_by_text("Flight Booking").click()
    popup = new_page.value
    flite = Flite_page(popup)
    flite.wait_for_load_state()
    expect(flite.page).to_have_title('QAClickJet - Flight Booking for Domestic and International, Cheap Air Tickets')
    return flite


def testflite_page_functionals(flite_page_obj):
    """Verify trip type options and select Round Trip if available."""
    flite_page_obj.select_round_trip_if_present()
    # ensure the trip options are visible after interaction
    expect(flite_page_obj.page.locator("//*[@id='ctl00_mainContent_rbtnl_Trip']")).to_be_visible()


def testflite_page_functionals_e2e(flite_page_obj):
    """End-to-end flight booking flow using the Flite_page POM with assertions."""
    fp = flite_page_obj
    fp.select_origin('BLR')
    fp.select_destination('GOI')
    fp.select_date('8', occurrence=1)
    fp.open_return_date_picker()
    fp.select_date('12', occurrence=2)

    # set passengers, then assert passenger info changes after applying a discount
    before = fp.get_passenger_counts()
    fp.set_passengers(adults=3, children=2)
    after_set = fp.get_passenger_counts()
    assert after_set == (3, 2), f"Expected (3,2) passengers, got {after_set}"

    fp.select_currency('USD')
    sel_curr = fp.get_selected_currency()
    assert sel_curr and sel_curr.upper() == 'USD', f"Expected USD, got {sel_curr}"

    fp.apply_discount('Senior Citizen')
    assert fp.is_discount_applied('Senior Citizen'), "Senior Citizen discount should be applied"
    assert fp.get_passenger_counts() == (3, 0), f"Expected (3,2) passengers, got {fp.get_passenger_counts()}"

@pytest.fixture
def topdeals_page(page, context):
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/")
    with context.expect_page() as new_page:
        page.get_by_text("Top Deals").click()
    top_deals = new_page.value
    top_deals_page = TopDeals_page(top_deals)
    top_deals_page.wait_for_load_state()
    expect(top_deals_page.page).to_have_title("GreenKart - veg and fruits kart")
    return  top_deals_page



def test_topdeals_page_functionals_e2e(topdeals_page):
    search_product = random.choice(testdata_for_search)
    topdeals_page.search(search_product)
    expect(topdeals_page.page.locator("(//tr/td[1])[1]")).to_contain_text(search_product.capitalize())
    name, price, discount_price = topdeals_page.first_row_text()
    print(f"price of an {name} is {price} and discount price is {discount_price}")


def test_login(page) -> None:
    page.goto("https://practicetestautomation.com/practice-test-login/")
    page.get_by_text("Home Practice Courses Blog Contact open menu Test login This is a simple Login").click()
    login_page = Login_page(page)
    login_page.login("student", "Password123")
    expect(page.get_by_role("heading")).to_contain_text("Logged In Successfully")
    expect(page.get_by_role("link", name="Log out")).to_be_visible()
    expect(page.get_by_role("link", name="Practice Test Automation", exact=True)).to_be_visible()
    page.get_by_role("link", name="Log out").click()

def test_login_by_extract(page) -> None:
    page.goto("https://practicetestautomation.com/practice-test-login/")
    credentials = [page.locator("(//*[@id='login']/ul/li[2]/b)[1]").text_content(),
                   page.locator("(//*[@id='login']/ul/li[2]/b)[2]").text_content()]
    login_page = Login_page(page)
    login_page.login(credentials[0], credentials[1])
    expect(page.get_by_role("heading")).to_contain_text("Logged In Successfully")
    expect(page.get_by_role("link", name="Log out")).to_be_visible()
    expect(page.get_by_role("link", name="Practice Test Automation", exact=True)).to_be_visible()
    page.get_by_role("link", name="Log out").click()


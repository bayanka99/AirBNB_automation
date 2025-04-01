import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


def got_to_tel_aviv_with_2_adults(page):
    page.goto("https://www.airbnb.com")

    page.wait_for_selector("#bigsearch-query-location-input", timeout=50000)

    page.fill("#bigsearch-query-location-input", "tel aviv")

    page.wait_for_selector("[data-testid='structured-search-input-field-guests-button']", timeout=50000)
    page.click("[data-testid='structured-search-input-field-guests-button']")
    page.wait_for_selector("[data-testid='stepper-adults-increase-button']", timeout=50000)
    page.click("[data-testid='stepper-adults-increase-button']")
    page.click("[data-testid='stepper-adults-increase-button']")

    page.click("[data-testid='structured-search-input-search-button']")
    page.wait_for_timeout(5000)

def test_case_2_airbnb_search_and_reserve(page):
    got_to_tel_aviv_with_2_adults(page)
    page.wait_for_selector("[itemprop='itemListElement']", timeout=50000)

    items = page.query_selector_all("[itemprop='itemListElement']")

    max_rating = 0.0
    max_rating_element = None

    for item in items:

        rating_element = item.query_selector(".r4a59j5")
        if rating_element:

            rating_text = rating_element.inner_text()
            if "out of" in rating_text:
                rating_value = float(rating_text.split(" ")[0])

                if rating_value > max_rating:
                    max_rating = rating_value
                    max_rating_element = item

    max_rating_element.click()
    new_tab = page.context.wait_for_event("page")
    new_tab.wait_for_timeout(5000)
    popup_button = new_tab.query_selector(f"xpath=/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button")
    if popup_button:
        popup_button.click()

    price_locator = new_tab.locator('span._hb913q').first
    price_text = price_locator.text_content()
    date_locator_check_in = new_tab.locator(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/button/div[1]/div[2]')
    date_locator_check_out = new_tab.locator(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/button/div[2]/div[2]')
    guests_locator = new_tab.locator(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/label/div[2]/div')
    nights_price = new_tab.locator(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[1]/span[2]')
    airbnb_service = new_tab.locator(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[2]/span[2]')
    total_price = new_tab.locator(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[2]/div/span[2]/span[1]/span')

    print()
    print("Reservation Details for the apartment with the highest rating:")
    print(f"price per night: {price_text}")
    print(f"Check-in Date: {date_locator_check_in.text_content()}")
    print(f"Check-out Date: {date_locator_check_out.text_content()}")
    print(f"guest count: {guests_locator.text_content()}")
    print(f"price for all nights: {nights_price.text_content()}")
    print(f"airbnb service: {airbnb_service.text_content()}")
    print(f"total price: {total_price.text_content()}")

    new_tab.click(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/button/span[1]/span')
    new_tab.fill('input[name="phoneInputphone-login"]', "123456789")
    new_tab.click(
        'xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div/main/div/div/div/div[1]/div[2]/div/div[1]/div/div[7]/div/div/div/div[2]/div/div/div/form/div/div[4]/button/span[1]/span')

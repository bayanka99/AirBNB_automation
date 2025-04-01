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


def got_to_tel_aviv_with_2_adults_and_1_child(page):
    page.goto("https://www.airbnb.com")

    page.wait_for_selector("#bigsearch-query-location-input", timeout=50000)

    page.fill("#bigsearch-query-location-input", "tel aviv")

    page.wait_for_selector("[data-testid='structured-search-input-field-guests-button']", timeout=50000)
    page.click("[data-testid='structured-search-input-field-guests-button']")
    page.wait_for_selector("[data-testid='stepper-adults-increase-button']", timeout=50000)
    page.click("[data-testid='stepper-adults-increase-button']")
    page.click("[data-testid='stepper-adults-increase-button']")
    page.click("[data-testid='stepper-children-increase-button']")

    page.click("[data-testid='structured-search-input-search-button']")
    page.wait_for_timeout(5000)

def get_max_rating_element(items):
    max_rating = 0.0
    max_rating_element = None
    for item in items:
        rating_element = item.query_selector(".r4a59j5")
        if rating_element:
            rating_text = rating_element.inner_text()
            #sometimes it might be "new" which is not a valid rating, there is a rating only if it contains "out of"
            if "out of" in rating_text:
                rating_value = float(rating_text.split(" ")[0])
                if rating_value > max_rating:
                    max_rating = rating_value
                    max_rating_element = item
    return max_rating_element


def print_reservation_box_details(page):
    price_locator = page.locator('span._hb913q').first
    price_text = price_locator.text_content()
    date_locator_check_in = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/button/div[1]/div[2]')
    date_locator_check_out = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/button/div[2]/div[2]')
    guests_locator = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/label/div[2]/div')
    price_blocks_locator = page.locator('div._14omvfj')

    titles_and_prices = list()
    # loop through each component in total price and extract the component's price and title
    for block in price_blocks_locator.all():
        title = block.locator('div._10d7v0r button div.l1x1206l').text_content()
        amount = block.locator('span._1k4xcdh').text_content()
        titles_and_prices.append([title,amount])

    total_price = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[2]/div/span[2]/span[1]/span')

    print()
    print("Reservation Details for the apartment with the highest rating:")
    print(f"price per night: {price_text}")
    print(f"Check-in Date: {date_locator_check_in.text_content()}")
    print(f"Check-out Date: {date_locator_check_out.text_content()}")
    print(f"guest count: {guests_locator.text_content()}")
    for title_and_price in titles_and_prices:
        print(f"{title_and_price[0]}: {title_and_price[1]}")
    print(f"total price: {total_price.text_content()}")


def test_case_2_airbnb_search_and_reserve(page):
    got_to_tel_aviv_with_2_adults_and_1_child(page)
    page.wait_for_selector("[itemprop='itemListElement']", timeout=50000)

    #this is the list of items as a result of the search query
    items = page.query_selector_all("[itemprop='itemListElement']")
    max_rating_element=get_max_rating_element(items)

    max_rating_element.click()
    new_tab = page.context.wait_for_event("page")
    new_tab.wait_for_timeout(5000)
    #sometimes a pop-up shows that informs that some information has been translated, which must be closed to continue our test
    popup_button = new_tab.query_selector(f"xpath=/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button")
    if popup_button:
        popup_button.click()

    print_reservation_box_details(new_tab)

    new_tab.click('xpath=/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/button/span[1]/span')
    new_tab.fill('input[name="phoneInputphone-login"]', "123456789")
    new_tab.click('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div/main/div/div/div/div[1]/div[2]/div/div[1]/div/div[7]/div/div/div/div[2]/div/div/div/form/div/div[4]/button/span[1]/span')

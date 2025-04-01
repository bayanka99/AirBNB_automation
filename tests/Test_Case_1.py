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


def test_case_1_airbnb_search_and_analyze_results(page):
    got_to_tel_aviv_with_2_adults(page)

    page.wait_for_selector("[itemprop='itemListElement']", timeout=50000)

    items = page.query_selector_all("[itemprop='itemListElement']")


    max_rating = 0.0
    title=""
    subtitle=""
    room_description=""
    date_description = ""
    price=""
    total_price=""

    for item in items:

        rating_element = item.query_selector(".r4a59j5")
        if rating_element:

            rating_text = rating_element.inner_text()
            if "out of" in rating_text:
                rating_value = float(rating_text.split(" ")[0])

                if rating_value > max_rating:
                    max_rating = rating_value
                    title=item.query_selector("[data-testid='listing-card-title']").inner_text()
                    subtitle = item.query_selector("[data-testid='listing-card-subtitle']").inner_text()
                    subtitle_spans = item.query_selector_all("[data-testid='listing-card-subtitle'] span span")
                    if len(subtitle_spans) > 0:
                        room_description = subtitle_spans[0].inner_text()
                    if len(subtitle_spans) > 4 :
                        date_description = subtitle_spans[3].inner_text()
                    price = item.query_selector("span._hb913q").inner_text()
                    total_price = item.query_selector("div._tt122m span[aria-hidden='true']").inner_text()
    print()
    print("details about the apartment with the highest rating:")
    print(f"title: {title}")
    print(f"subtitle: {subtitle}")
    print(f"room description: {room_description}")
    print(f"date description: {date_description}")
    print(f"price per night: {price}")
    print(f"total price: {total_price}")


    page.click("[data-testid='category-bar-filter-button']")
    max_price=45
    while True:
        page.fill("#price_filter_max", str(max_price+1))
        page.wait_for_timeout(100)
        max_price+=1
        page.click("#price_filter_max-label")

        show_places_link = page.locator(
            'xpath=/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/footer/div/a')

        link_text = show_places_link.inner_text()
        while link_text=="loading":
            link_text = show_places_link.inner_text()

        if any(char.isdigit() for char in link_text):
            places_count = int(''.join(filter(str.isdigit, link_text)))
            if places_count > 0:
                break


    page.click('xpath=/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/footer/div/a')


    title = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[1]').inner_text()

    subtitle = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/span[1]/span[1]').inner_text()


    room_description = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[3]').inner_text()


    date_description = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[4]/span/span[1]').inner_text()


    price_per_night = page.locator('span.a8jt5op.atm_3f_idpfg4.atm_7h_hxbz6r.atm_7i_ysn8ba.atm_e2_t94yts.atm_ks_zryt35.atm_l8_idpfg4.atm_vv_1q9ccgz.atm_vy_t94yts.aze35hn.atm_mk_stnw88.atm_tk_idpfg4.dir.dir-ltr')
    if price_per_night.count() == 0:
        price_per_night = page.locator('span.a8jt5op.atm_3f_idpfg4.atm_7h_hxbz6r.atm_7i_ysn8ba.atm_e2_t94yts.atm_ks_zryt35.atm_l8_idpfg4.atm_vv_1q9ccgz.atm_vy_t94yts.a1ugchtf.atm_mk_stnw88.atm_tk_idpfg4.dir.dir-ltr')

    price=price_per_night.inner_text()
    total_price = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[5]/div[2]/div/div/span[3]/div/button/div/div').inner_text()


    print()
    print("details about the apartment with the lowest price:")
    print(f"title: {title}")
    print(f"subtitle: {subtitle}")
    print(f"room description: {room_description}")
    print(f"date description: {date_description}")
    print(f"price per night: {price}")
    print(f"total price: {total_price}")



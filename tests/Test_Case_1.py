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

def test_case_1_airbnb_search_and_analyze_results(page):

    page.goto("https://www.airbnb.com")



    page.wait_for_selector("#bigsearch-query-location-input", timeout=50000)



    page.fill("#bigsearch-query-location-input", "tel aviv")

    page.wait_for_selector("[data-testid='structured-search-input-field-guests-button']", timeout=50000)
    page.click("[data-testid='structured-search-input-field-guests-button']")
    page.wait_for_selector("[data-testid='stepper-adults-increase-button']", timeout=50000)
    page.click("[data-testid='stepper-adults-increase-button']")
    page.click("[data-testid='stepper-adults-increase-button']")

    page.click("[data-testid='structured-search-input-search-button']")

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
                print(f"Found {places_count} places!")
                break


    page.click('xpath=/html/body/div[9]/div/div/section/div/div/div[2]/div/div[2]/footer/div/a')
    try:

        room_title = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[1]').inner_text()
        print(f"Room title: {room_title}")
        subtitle = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/span[1]/span[1]').inner_text()
        print(f"Subtitle: {subtitle}")
        room_description = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[3]').inner_text()
        print(f"Room description: {room_description}")

        date_range = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[4]/span/span[1]').inner_text()
        print(f"Date range: {date_range}")

        price_per_night = page.locator('span.a8jt5op.atm_3f_idpfg4.atm_7h_hxbz6r.atm_7i_ysn8ba.atm_e2_t94yts.atm_ks_zryt35.atm_l8_idpfg4.atm_vv_1q9ccgz.atm_vy_t94yts.aze35hn.atm_mk_stnw88.atm_tk_idpfg4.dir.dir-ltr')
        if price_per_night.count() == 0:
            price_per_night = page.locator('span.a8jt5op.atm_3f_idpfg4.atm_7h_hxbz6r.atm_7i_ysn8ba.atm_e2_t94yts.atm_ks_zryt35.atm_l8_idpfg4.atm_vv_1q9ccgz.atm_vy_t94yts.a1ugchtf.atm_mk_stnw88.atm_tk_idpfg4.dir.dir-ltr')
        print(price_per_night.inner_text())

        total_price = page.locator('xpath=/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div[5]/div[2]/div/div/span[3]/div/button/div/div').inner_text()
        print(total_price)


    except Exception as e:
        print(f"Error extracting details: {e}")

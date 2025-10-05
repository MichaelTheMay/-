from camoufox.sync_api import amoufox
import json, re, time

INITIAL_URL = 'https://www.google.com/maps/search/restaurants/@40.7500474,-74.0132272,12z/data=!4m2!2m1!6e5'

def scrape_google_maps(url=INITIAL_URL, outfile="results.json"):
    config = {
        'window.outerHeight': 1056, 'window.outerWidth': 1920,
        'window.innerHeight': 1008, 'window.innerWidth': 1920,
        'navigator.userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'navigator.platform': 'Win32', 'navigator.hardwareConcurrency': 12,
        'navigator.language': 'en-US', 'navigator.languages': ['en-US'],
    }

    with Camoufox(headless=True, os="windows", config=config, i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('div[role=feed]')

        # Auto-scroll to load all results
        last_height, same_count = 0, 0
        while same_count < 3:  # stop after 3 attempts with no new results
            page.mouse.wheel(0, 4000)
            time.sleep(2)
            new_height = page.evaluate("document.querySelector('div[role=feed]').scrollHeight")
            if new_height == last_height:
                same_count += 1
            else:
                same_count = 0
                last_height = new_height

        # Extract in parallel
        divs = page.locator('div[role=feed] div.Nv2PK').all()

        results = []
        for div in divs:
            try:
                name = div.locator('a.hfpxzc').get_attribute('aria-label')
                link = div.locator('a.hfpxzc').get_attribute('href')
                rating = div.locator('span.MW4etd').inner_text()
                reviews = div.locator('span.UY7F9').inner_text()
                results.append({
                    'name': name,
                    'link': link,
                    'rating': float(rating) if rating else None,
                    'reviews': int(re.sub(r'[\(\),]', '', reviews)) if reviews else None
                })
            except Exception as e:
                continue

        # Save incrementally
        with open(outfile, 'w', encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        page.close()

if __name__ == "__main__":
    scrape_google_maps()
``
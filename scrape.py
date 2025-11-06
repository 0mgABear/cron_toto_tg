from playwright.sync_api import sync_playwright
import re

def scrape_next_draw():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx",
            wait_until="networkidle"
        )

        text = page.inner_text("body")

        jackpot_match = re.search(r"Next Jackpot\s*\$[0-9,]+ est", text)
        jackpot = jackpot_match.group() if jackpot_match else "Not found"

        draw_match = re.search(r"Next Draw\s*\n?\s*.*,\s*\d{1,2}\s*[A-Za-z]{3}\s*\d{4}\s*,\s*\d{1,2}\.\d{2}[ap]m", text)
        draw = draw_match.group().replace("\n", " ").strip() if draw_match else "Not found"

        browser.close()
        return jackpot, draw

if __name__ == "__main__":
    jackpot, draw = scrape_next_draw()
    print(f"Jackpot: {jackpot}")
    print(f"Draw: {draw}")

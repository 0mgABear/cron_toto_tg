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

        # Match "Next Jackpot" and capture the number part
        jackpot_match = re.search(r"Next Jackpot\s*\$([0-9,]+)\s*est", text)
        if jackpot_match:
            jackpot_amount = jackpot_match.group(1)  # capture group: just the number
            jackpot = f"Next Jackpot: ${jackpot_amount} est"
        else:
            jackpot_amount = None
            jackpot = "Next Jackpot: Not found"

        # Match "Next Draw" line
        draw_match = re.search(
            r"Next Draw\s*\n?\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*\d{1,2}\s*[A-Za-z]{3}\s*\d{4}\s*,\s*\d{1,2}\.\d{2}[ap]m",
            text
        )
        draw = draw_match.group().replace("\n", " ").strip() if draw_match else "Next Draw: Not found"

        browser.close()
        return jackpot, jackpot_amount, draw


if __name__ == "__main__":
    jackpot, jackpot_amount, draw = scrape_next_draw()
    print(jackpot)
    print(draw)
    print(f"(Extracted amount only: {jackpot_amount})")

"""
Cricbuzz Live Score — capture live cricket scores with Playwright.

Opens cricbuzz.com in a real browser, waits for the match cards that
JavaScript loads in, prints the score of every live match, and saves
a screenshot as score.png.

Run headed (you can watch the browser):   python cricbuzz_score.py
Run headless (no window):                 python cricbuzz_score.py --headless

Selectors (found with right-click → Inspect on cricbuzz.com):
  Match card   : <a class="... bg-cbWhite ..." href="/live-cricket-scores/...">
  Live status  : <span class="text-cbLive ...">  (only live matches have it)
"""

import sys

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

URL = "https://www.cricbuzz.com/"
CARD = 'a.bg-cbWhite[href*="/live-cricket-scores/"]'
LIVE_CARD = f"{CARD}:has(span.text-cbLive)"
SCREENSHOT = "score.png"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
WAIT_MS = 30_000  # wait at most 30 s for the cards; returns as soon as they appear


def clean_card_text(text):
    """Turn a card's text into tidy lines: 'TEAM score', next team, status."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # lines look like: [series, format, TEAM1, score1, TEAM2, (score2), status]
    out = []
    i = 2  # skip series name and format badge
    while i < len(lines) - 1:
        team = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) - 1 else ""
        if nxt and any(ch.isdigit() for ch in nxt):  # a score like 317-8 (49)
            out.append(f"{team} {nxt}")
            i += 2
        else:
            out.append(team)  # team hasn't batted yet
            i += 1
    out.append(lines[-1])  # status line, e.g. "India need 24 runs in 28 balls"
    return out


def main():
    headless = "--headless" in sys.argv

    with sync_playwright() as p:
        # Cricbuzz returns "Access Denied" to Playwright's default headless
        # browser. Using the full Chromium (channel="chromium") with a normal
        # user agent (instead of "HeadlessChrome") lets headless mode load it.
        browser = p.chromium.launch(headless=headless, channel="chromium")
        page = browser.new_page(
            viewport={"width": 1366, "height": 900},
            user_agent=USER_AGENT,
        )

        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=60_000)

            # Wait for the thing we need (the match cards), not a fixed sleep.
            try:
                page.wait_for_selector(CARD, timeout=WAIT_MS)
            except PlaywrightTimeout:
                print("Could not find any match cards on Cricbuzz.")
                print("The site may be slow, blocking the browser, or its layout changed.")
                page.screenshot(path=SCREENSHOT)
                print(f"saved {SCREENSHOT} (check it to see what loaded)")
                return 1

            live_cards = page.locator(LIVE_CARD)
            count = live_cards.count()

            if count == 0:
                print("No match is live right now.")
            else:
                for n in range(count):
                    card = live_cards.nth(n)
                    title = (card.get_attribute("title") or "").strip()
                    if n:
                        print()
                    print(f"[{title}]")
                    print("\n".join(clean_card_text(card.inner_text())))

            page.screenshot(path=SCREENSHOT)
            print(f"\nsaved {SCREENSHOT}")
            return 0
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())

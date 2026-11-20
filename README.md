# Python Basics

Small Python projects I built while learning the language. Each folder is a
self-contained program you can run on its own.

## Projects

### [grade-manager](grade-manager/)
A terminal app that stores student marks, works out each grade (A–E), and
prints an aligned results table with the class average, highest and lowest
mark. Invalid input (blank names, duplicates, marks outside 0–100, text
instead of numbers) is handled without crashing.

Uses only plain Python, nothing to install.

```bash
cd grade-manager
python grade_manager.py
```

### [cricket-score](cricket-score/)
Fetches live cricket scores from Cricbuzz with [Playwright](https://playwright.dev/python/).
The scores are loaded by JavaScript after the page opens, so the script drives
a real browser, waits for the score cards to appear (no fixed sleeps), prints
every live match, and saves a screenshot as `score.png`. If no match is live,
it says so instead of failing.

```bash
cd cricket-score
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

python cricbuzz_score.py              # opens a browser window
python cricbuzz_score.py --headless   # runs without a window
```

## What I practised
- Lists, dictionaries, functions and loops
- Validating user input and handling errors
- Formatting output with f-strings
- Browser automation and waiting for dynamic content with Playwright

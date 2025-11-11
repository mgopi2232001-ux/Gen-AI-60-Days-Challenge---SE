import asyncio, random, os, re 
from playwright.async_api import async_playwright

QUERY = "india vs sa womens 2025 worldcup cricbuzz"
SCORECARD_XPATH = '//*[@id="main-nav"]/a[3]'                 # Scorecard tab (your XPath)
DATA_XPATH = '/html/body/div/main/div/div[2]/div[1]'         # Block to extract (your XPath)

OUTPUT_DIR = r"C:\Users\mgopi\OneDrive\Desktop\Python-Practice\Playwright"
OUTPUT_FILE = "scorecard_INDW_batting.csv"                   # <-- only India batting

SEARCH = {
    "url": "https://duckduckgo.com/",
    "input": 'input[name="q"]',
    "result_links": "a[data-testid='result-title-a'], h2 a.result__a, .results a.result__a",
    "site_query": lambda q: f"site:cricbuzz.com {q}",
}

def _pad(row, widths):
    return " | ".join(c.ljust(w) for c, w in zip(row, widths))

async def wait_for_scorecard(page):
    try:
        await page.wait_for_url("**/live-cricket-scorecard/**", timeout=8000)
        return
    except:
        pass
    for sel in [".cb-scrd-hdr-rw",".cb-scrd-lft-col",".cb-scrd-rght-col","text=Fall of Wickets"]:
        try:
            await page.locator(sel).first.wait_for(timeout=6000)
            return
        except:
            continue
    try:
        await page.locator(f"xpath={DATA_XPATH}").first.wait_for(timeout=6000)
    except:
        pass

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        ctx = await browser.new_context(
            viewport={"width": 1366, "height": 860},
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"),
            locale="en-US",
            timezone_id="Asia/Kolkata",
        )
        page = await ctx.new_page()

        async def do_query(q: str):
            await page.goto(SEARCH["url"], wait_until="domcontentloaded")
            box = page.locator(SEARCH["input"])
            await box.wait_for()
            await box.click()
            for ch in q:
                await page.keyboard.type(ch, delay=random.randint(20, 70))
            await page.keyboard.press("Enter")
            await page.wait_for_selector(SEARCH["result_links"], timeout=15000)

        async def click_cricbuzz_or_retry():
            links = page.locator(SEARCH["result_links"])
            for i in range(await links.count()):
                href = await links.nth(i).get_attribute("href")
                if href and "cricbuzz.com" in href.lower():
                    await links.nth(i).click()
                    await page.wait_for_load_state("domcontentloaded")
                    return True
            await do_query(SEARCH["site_query"](QUERY))
            links = page.locator(SEARCH["result_links"])
            for i in range(await links.count()):
                href = await links.nth(i).get_attribute("href")
                if href and "cricbuzz.com" in href.lower():
                    await links.nth(i).click()
                    await page.wait_for_load_state("domcontentloaded")
                    return True
            return False

        # 1) Search → open Cricbuzz
        await do_query(QUERY)
        if not await click_cricbuzz_or_retry():
            raise RuntimeError("No Cricbuzz link found in search results.")

        # 2) Click Scorecard tab
        tab = page.locator(f"xpath={SCORECARD_XPATH}")
        await tab.first.wait_for(timeout=15000)
        await tab.first.click()
        await wait_for_scorecard(page)

        # 3) Parse tables under your block and render as fixed-width text (unchanged)
        container = page.locator(f"xpath={DATA_XPATH}")
        await container.first.wait_for(timeout=20000)

        tables = container.locator("table")
        tcount = await tables.count()

        lines_out = []
        if tcount == 0:
            # Fallback: if no tables, at least dump readable text
            txt = (await container.first.inner_text()) or ""
            lines_out.append(txt.strip())
        else:
            for t_idx in range(tcount):
                table = tables.nth(t_idx)

                # optional: add a visible heading if present near table
                try:
                    heading = await table.locator("xpath=preceding-sibling::*[self::h2 or self::h3 or contains(@class,'cb-scrd-hdr-rw')][1]").first.inner_text(timeout=1000)
                    if heading:
                        lines_out.append(heading.strip())
                except:
                    pass

                rows = table.locator("tr")
                rcount = await rows.count()
                matrix = []
                for r in range(rcount):
                    row = rows.nth(r)
                    cells = row.locator("th, td")
                    ccount = await cells.count()
                    values = []
                    for c in range(ccount):
                        v = await cells.nth(c).inner_text()
                        v = (v or "").strip()
                        v = re.sub(r"\s+", " ", v)  # collapse internal whitespace
                        values.append(v)
                    if any(values):  # skip empty rows
                        matrix.append(values)

                if not matrix:
                    continue

                # normalize columns (ragged rows → pad)
                max_cols = max(len(r) for r in matrix)
                for r in matrix:
                    if len(r) < max_cols:
                        r.extend([""] * (max_cols - len(r)))

                # compute column widths
                widths = [0] * max_cols
                for r in matrix:
                    for i, cell in enumerate(r):
                        widths[i] = max(widths[i], len(cell))

                # build pretty table
                sep = "-+-".join("-" * w for w in widths)
                # detect header row if first row is th’s (best effort)
                first_row_has_th = False
                try:
                    first_th_count = await rows.nth(0).locator("th").count()
                    first_row_has_th = first_th_count > 0
                except:
                    pass

                for i_row, r in enumerate(matrix):
                    line = _pad(r, widths)
                    lines_out.append(line)
                    if i_row == 0 and first_row_has_th:
                        lines_out.append(sep)

                # spacing between tables
                lines_out.append("")

        # 4) SAVE ONLY INDIA (INDW) BATTING AS CSV
        import csv

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

        # Flatten to tokens (one item per visible line)
        blob = "\n".join(lines_out)
        blob = blob.replace("\xa0", " ").replace("Â", " ")  # fix nbsp artifacts
        tokens = [t.strip() for t in blob.splitlines() if t.strip()]

        # Find the INDW section and the "Batter" block under it; ignore RSAW completely
        i = 0
        found_indw = False
        # seek INDW
        while i < len(tokens):
            if tokens[i].strip().upper() == "INDW":
                found_indw = True
                i += 1
                break
            i += 1

        if not found_indw:
            raise RuntimeError("INDW section not found in parsed text.")

        # skip optional scoreline right after INDW (e.g., '298-7 (50 Ov)')
        if i < len(tokens) and ("Ov" in tokens[i] or "Overs" in tokens[i]):
            i += 1

        # seek 'Batter' header
        while i < len(tokens) and tokens[i].lower() != "batter":
            i += 1
        if i >= len(tokens):
            raise RuntimeError("Batter section not found under INDW.")

        # skip the column labels printed on separate lines: R, B, 4s, 6s, SR
        cols = {"r","b","4s","6s","sr"}
        j = i + 1
        while j < len(tokens) and tokens[j].lower() in cols:
            j += 1
        i = j

        # write CSV
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Batter","Dismissal","R","B","4s","6s","SR"])

            # parse batter rows until we hit Extras/Total/Did not Bat/Bowler or a new team
            def numberish(x):
                return bool(re.fullmatch(r"[0-9]+(?:\.[0-9])?", x)) or bool(re.fullmatch(r"\d{1,3}-\d{1,2}", x))

            while i < len(tokens):
                t = tokens[i].lower()
                if t in ("extras","total","did not bat","bowler","fall of wickets","powerplays","partnerships","info","rsaw"):
                    break

                # expect name, dismissal, R, B, 4s, 6s, SR
                if i + 6 < len(tokens):
                    name = tokens[i]
                    dismissal = tokens[i+1]
                    R, Bv, F, Sx, SR = tokens[i+2], tokens[i+3], tokens[i+4], tokens[i+5], tokens[i+6]
                    if numberish(R) and numberish(Bv):
                        w.writerow([name, dismissal, R, Bv, F, Sx, SR])
                        i += 7
                        continue

                i += 1

            # Extras (optional)
            if i < len(tokens) and tokens[i].lower() == "extras":
                detail = tokens[i+1] if i+1 < len(tokens) else ""
                w.writerow(["Extras","",detail,"","","",""])
                i += 2

            # Total (optional)
            if i < len(tokens) and tokens[i].lower() == "total":
                detail = tokens[i+1] if i+1 < len(tokens) else ""
                w.writerow(["Total","",detail,"","","",""])
                i += 2

            # Did not Bat (optional)
            if i < len(tokens) and tokens[i].lower() == "did not bat":
                detail = tokens[i+1] if i+1 < len(tokens) else ""
                w.writerow(["Did not Bat","",detail,"","","",""])
                i += 2

        print("✅ INDW batting CSV saved at:", out_path)

        await page.wait_for_timeout(1200)
        await ctx.close(); await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://afltables.com/afl/seas/{year}.html"
OUT_DIR = Path("data/years")                 # per-year CSVs live here
COMBINED_CSV = Path("data/afl_ladder_with_premiers.csv")
REQUEST_DELAY_SEC = 1                        # be polite to the host
START_YEAR = 1966

def current_year() -> int:
    """Return system current year."""
    return datetime.now().year

def fetch_soup(url: str) -> BeautifulSoup:
    """Fetch a URL and return a BeautifulSoup parser."""
    headers = {
        "User-Agent": "Mozilla/5.0 (+https://github.com/requests/requests)"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def parse_grand_final_winner(soup: BeautifulSoup) -> Optional[str]:
    """
    Return the Grand Final winner.
    Handles drawn GF + replay by scanning all 'Grand Final' <b> blocks from the end.
    Uses the next actual <table> after the heading table (not just next_sibling).
    Looks for any <td> containing 'won by' and takes the text before that.
    """
    try:
        gf_heads = [b for b in soup.find_all("b") if "Grand Final" in b.get_text()]
        for b in reversed(gf_heads):
            parent_table = b.find_parent("table")
            if not parent_table:
                continue

            # Find the next actual table in the DOM after the heading table
            grand_table = parent_table.find_next(lambda t: t.name == "table")
            if not grand_table:
                continue

            for row in grand_table.find_all("tr"):
                for td in row.find_all("td"):
                    txt = td.get_text(" ", strip=True)
                    low = txt.lower()
                    if " won by" in low:
                        # Extract winner name before ' won by'
                        cut = low.find(" won by")
                        # Use the original-case string up to the same index
                        return txt[:cut].strip()
    except Exception:
        pass

    # Fallback: search globally for 'won by'
    try:
        for td in soup.find_all("td"):
            txt = td.get_text(" ", strip=True)
            low = txt.lower()
            if "grand final" in low and " won by" in low:
                cut = low.find(" won by")
                return txt[:cut].strip()
    except Exception:
        pass

    return None


def find_ladder_table(soup: BeautifulSoup):
    """
    Locate the ladder table. AFL Tables pages contain many tables;
    we pick the first whose text includes 'Ladder' and has <th> headers.
    """
    for table in soup.find_all("table"):
        if table.find("th") and "Ladder" in table.get_text():
            return table
    return None

def scrape_year(year: int) -> pd.DataFrame:
    """Scrape one year and return a DataFrame of ladder rows."""
    url = BASE_URL.format(year=year)
    print(f"Scraping {year} -> {url}")
    soup = fetch_soup(url)

    winner = parse_grand_final_winner(soup)

    ladder_table = find_ladder_table(soup)
    if ladder_table is None:
        print(f"  ! Ladder table not found for {year}")
        return pd.DataFrame()

    rows = []
    # Skip first 2 rows: title row + header row
    for tr in ladder_table.find_all("tr")[2:]:
        tds = tr.find_all("td")
        if len(tds) < 14:
            continue

        team_name = tds[1].get_text(strip=True)
        is_premier = bool(winner and winner.lower() in team_name.lower())

        rows.append({
            "Year": year,
            "Position": tds[0].get_text(strip=True),
            "Team": team_name,
            "Played": tds[2].get_text(strip=True),
            "Wins": tds[3].get_text(strip=True),
            "Draws": tds[4].get_text(strip=True),
            "Losses": tds[5].get_text(strip=True),
            "For": tds[9].get_text(strip=True),
            "Against": tds[11].get_text(strip=True),
            "Percentage": tds[12].get_text(strip=True),
            "Points": tds[13].get_text(strip=True),
            "Premiers": is_premier,
        })

    return pd.DataFrame(rows)

def save_year_csv(year: int, df: pd.DataFrame) -> Path:
    """Save a single year CSV and return its path."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"afl_{year}.csv"
    df.to_csv(path, index=False)
    print(f"  ✓ Saved {path}")
    return path

def build_combined_csv() -> None:
    """Concatenate all per-year CSVs into one combined CSV."""
    if not OUT_DIR.exists():
        print("No year directory found; skipping combined CSV.")
        return

    frames: List[pd.DataFrame] = []
    for p in sorted(OUT_DIR.glob("afl_*.csv")):
        try:
            frames.append(pd.read_csv(p))
        except Exception as e:
            print(f"  ! Skipping {p}: {e}")

    if not frames:
        print("No year CSVs to combine.")
        return

    combined = pd.concat(frames, ignore_index=True)
    COMBINED_CSV.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(COMBINED_CSV, index=False)
    print(f"✓ Wrote combined CSV -> {COMBINED_CSV} ({len(combined)} rows)")

def main():
    cy = current_year()
    total_rows = 0

    for year in range(START_YEAR, cy + 1):
        year_csv = OUT_DIR / f"afl_{year}.csv"

        # Re-scrape the current year every run; for past years, reuse if present.
        if year != cy and year_csv.exists():
            print(f"Skipping {year} (already scraped).")
        else:
            df_year = scrape_year(year)
            if df_year.empty:
                print(f"  ! No rows for {year}.")
            else:
                save_year_csv(year, df_year)
                total_rows += len(df_year)
            time.sleep(REQUEST_DELAY_SEC)

    # Always (re)build the combined CSV so it includes any new current-year rows.
    build_combined_csv()
    print(f"Done. Newly scraped rows this run: {total_rows}")

if __name__ == "__main__":
    main()

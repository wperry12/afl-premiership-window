import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

YEARS = range(1966, 2026)
ladder_data = []

for year in YEARS:
    print(f"Scraping {year}...")
    url = f"https://afltables.com/afl/seas/{year}.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    ### --- Get Grand Final Winner --- ###
    grand_final_winner = None
    try:
        for b in soup.find_all("b"):
            if "Grand Final" in b.text:
                grand_table = b.find_parent("table").find_next_sibling("table")
                # print(grand_table)
                match_rows = grand_table.find_all("tr")
                for row in match_rows:
                    cells = row.find_all("td")
                    if len(cells) >= 4 and "won by" in cells[3].text:
                        winner_text = cells[3].text.strip()
                        grand_final_winner = winner_text.split(" won by")[0]
                        break
                break
    except Exception as e:
        print(f"Could not find Grand Final winner for {year}: {e}")
        continue

    ### --- Get Ladder Table --- ###
    try:
        all_tables = soup.find_all("table")
        ladder_table = None
        for table in all_tables:
            if table.find("th") and "Ladder" in table.text:
                ladder_table = table
                break

        if not ladder_table:
            print(f"Ladder not found for {year}")
            continue

        rows = ladder_table.find_all("tr")[2:]  # skip title + header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 14:
                continue
            team_name = cols[1].get_text(strip=True)
            is_premier = (grand_final_winner and grand_final_winner.lower() in team_name.lower())
            ladder_data.append({
                "Year": year,
                "Position": cols[0].get_text(strip=True),
                "Team": team_name,
                "Played": cols[2].get_text(strip=True),
                "Wins": cols[3].get_text(strip=True),
                "Draws": cols[4].get_text(strip=True),
                "Losses": cols[5].get_text(strip=True),
                "For": cols[9].get_text(strip=True),
                "Against": cols[11].get_text(strip=True),
                "Percentage": cols[12].get_text(strip=True),
                "Points": cols[13].get_text(strip=True),
                "Premiers": is_premier
            })

    except Exception as e:
        print(f"Error parsing ladder for {year}: {e}")

    time.sleep(1)

print(f"Total rows collected: {len(ladder_data)}")

# Save to CSV
df = pd.DataFrame(ladder_data)
df.to_csv("afl_ladder_with_premiers.csv", index=False)
print("Saved to 'afl_ladder_with_premiers.csv'")

import requests
import pandas as pd

def fetch_afl_ladder(year: int = 2025):
    url = "https://api.afl.com.au/cfs/afl/WM_LADDER"

    headers = {
        "x-media-mis-token": "afl",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Origin": "https://www.afl.com.au",
        "Referer": "https://www.afl.com.au/",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch ladder: {response.status_code}")

    data = response.json()
    ladders = data["Ladders"]
    ladder_for_year = None

    for ladder in ladders:
        if ladder["Season"]["Year"] == year:
            ladder_for_year = ladder["Teams"]
            break

    if ladder_for_year is None:
        raise Exception(f"No ladder found for {year}")

    rows = []
    for team in ladder_for_year:
        stats = team["Stats"]
        rows.append({
            "Team": team["Team"]["Name"],
            "Played": stats["Played"],
            "Wins": stats["Wins"],
            "Losses": stats["Losses"],
            "Draws": stats["Draws"],
            "For": stats["PointsFor"],
            "Against": stats["PointsAgainst"],
            "Percentage": stats["Percentage"],
            "LadderPosition": stats["LadderPosition"]
        })

    df = pd.DataFrame(rows)
    df.to_csv(f"afl_ladder_{year}.csv", index=False)
    print(f"Saved ladder to afl_ladder_{year}.csv")

if __name__ == "__main__":
    fetch_afl_ladder()

import pandas as pd

# Load the ladder data
df = pd.read_csv("afl_ladder_with_premiers.csv")

# Premiership window conventinally defined as top 6 for attack and defence
def is_in_window(team_row, year_df):
    # Convert For and Against columns to numeric
    year_df["For"] = pd.to_numeric(year_df["For"], errors="coerce")
    year_df["Against"] = pd.to_numeric(year_df["Against"], errors="coerce")
    
    # Get top 6 in "For" (points scored)
    top_scoring_teams = year_df.nlargest(6, "For")["Team"].tolist()
    
    # Get top 6 in "Against" (lowest points conceded)
    best_defensive_teams = year_df.nsmallest(6, "Against")["Team"].tolist()

    return (team_row["Team"] in top_scoring_teams) and (team_row["Team"] in best_defensive_teams)

def evaluate_window_method(df):
    correct = 0
    total = 0

    print("Evaluating window method...")
  
    for year in df["Year"].unique():
        year_df = df[df["Year"] == year].copy()
        premier_row = year_df[year_df["Premiers"] == True]
        
        if premier_row.empty:
            continue  # skip if no premier marked that year

        team_row = premier_row.iloc[0]
        total += 1
        if is_in_window(team_row, year_df):
            correct += 1
    
    print(f"Premiers matching window criteria: {correct}/{total}")
    print(f"Accuracy: {100 * correct / total:.2f}%")

if __name__ == "__main__":
    evaluate_window_method(df)

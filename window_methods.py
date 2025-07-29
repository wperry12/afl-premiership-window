import pandas as pd

# Load the ladder data
df = pd.read_csv("afl_ladder_with_premiers.csv")

# Premiership window conventinally defined as top 6 for attack and defence
# def is_in_window(team_row, year_df):
#     # Convert For and Against columns to numeric
#     year_df["For"] = pd.to_numeric(year_df["For"], errors="coerce")
#     year_df["Against"] = pd.to_numeric(year_df["Against"], errors="coerce")
    
#     # Get top 6 in "For" (points scored)
#     top_scoring_teams = year_df.nlargest(6, "For")["Team"].tolist()
    
#     # Get top 6 in "Against" (lowest points conceded)
#     best_defensive_teams = year_df.nsmallest(6, "Against")["Team"].tolist()

#     return (team_row["Team"] in top_scoring_teams) and (team_row["Team"] in best_defensive_teams)

def evaluate_window_method(df):
    correct = 0
    total = 0
    window_total = 0

    print("Evaluating window method...\n")
  
    for year in df["Year"].unique():
        year_df = df[df["Year"] == year].copy()
        premier_row = year_df[year_df["Premiers"] == True]
        
        if premier_row.empty:
            continue  # skip if no premier marked that year

        # Ensure numeric types
        year_df["For"] = pd.to_numeric(year_df["For"], errors="coerce")
        year_df["Against"] = pd.to_numeric(year_df["Against"], errors="coerce")
        year_df["Played"] = pd.to_numeric(year_df["Played"], errors="coerce")

        # Normalise
        year_df["AttackRate"] = year_df["For"] / year_df["Played"]
        year_df["DefenceRate"] = year_df["Against"] / year_df["Played"]

        # Calculate ranks
        year_df["AttackRank"] = year_df["AttackRate"].rank(method="min", ascending=False)
        year_df["DefenceRank"] = year_df["DefenceRate"].rank(method="min", ascending=True)

        # Define window (can adjust thresholds)
        year_df["InWindow"] = (year_df["AttackRank"] <= 6) & (year_df["DefenceRank"] <= 6)
        window_total += year_df["InWindow"].sum()

        # Evaluate premier
        team_row = premier_row.iloc[0]
        team_name = team_row["Team"]
        total += 1

        if year_df[year_df["Team"] == team_name]["InWindow"].iloc[0]:
            correct += 1
        else:
            attack_rank = int(year_df[year_df["Team"] == team_name]["AttackRank"].iloc[0])
            defence_rank = int(year_df[year_df["Team"] == team_name]["DefenceRank"].iloc[0])
            print(f"{year} — {team_name}: Attack Rank = {attack_rank}, Defence Rank = {defence_rank}")

    print(f"\nPremiers matching window criteria: {correct}/{total}")
    print(f"Total teams in window: {window_total}")
    print(f"Precision (premiers in window / teams in window): {100 * correct / window_total:.2f}%")
    print(f"Recall (premiers in window / total premiers): {100 * correct / total:.2f}%")




if __name__ == "__main__":
    evaluate_window_method(df)

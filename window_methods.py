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

    print("Evaluating window method...\n")
  
    for year in df["Year"].unique():
        year_df = df[df["Year"] == year].copy()
        premier_row = year_df[year_df["Premiers"] == True]
        
        if premier_row.empty:
            continue  # skip if no premier marked that year

        # Ensure numeric types
        year_df["For"] = pd.to_numeric(year_df["For"], errors="coerce")
        year_df["Against"] = pd.to_numeric(year_df["Against"], errors="coerce")

        team_row = premier_row.iloc[0]
        team_name = team_row["Team"]
        total += 1

        # Calculate attack and defence ranks
        year_df["AttackRank"] = year_df["For"].rank(method="min", ascending=False)
        year_df["DefenceRank"] = year_df["Against"].rank(method="min", ascending=True)

        attack_rank = int(year_df[year_df["Team"] == team_name]["AttackRank"].iloc[0])
        defence_rank = int(year_df[year_df["Team"] == team_name]["DefenceRank"].iloc[0])

        in_window = (attack_rank <= 6 and defence_rank <= 6)
        if in_window:
            correct += 1
        else:
            print(f"{year} — {team_name}: Attack Rank = {attack_rank}, Defence Rank = {defence_rank}")

    print(f"\nPremiers matching window criteria: {correct}/{total}")
    print(f"Accuracy: {100 * correct / total:.2f}%")


if __name__ == "__main__":
    evaluate_window_method(df)
